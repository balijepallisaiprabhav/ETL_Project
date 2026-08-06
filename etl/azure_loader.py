import os
import time

import pandas as pd
import pyodbc
from dotenv import load_dotenv


load_dotenv()


def load_to_azure(df: pd.DataFrame) -> None:
    connection = None

    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")

    if not all([server, database, username, password]):
        raise ValueError(
            "Azure SQL credentials are missing from the .env file."
        )

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=tcp:{server},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Authentication=SqlPassword;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=60;"
    )

    max_attempts = 5

    try:
        # Retry because an Azure serverless database may need time to wake up.
        for attempt in range(1, max_attempts + 1):
            try:
                print(
                    f"Connecting to Azure SQL Database "
                    f"(attempt {attempt}/{max_attempts})..."
                )

                connection = pyodbc.connect(
                    connection_string,
                    timeout=60
                )

                print("Connected to Azure SQL Database.")
                break

            except pyodbc.Error as error:
                if attempt == max_attempts:
                    raise

                print("Azure SQL is temporarily unavailable.")
                print("Retrying after 15 seconds...")
                print(error)
                time.sleep(15)

        cursor = connection.cursor()

        # Create the Employees table when it does not already exist.
        cursor.execute(
            """
            IF OBJECT_ID('dbo.Employees', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.Employees
                (
                    EmployeeID INT PRIMARY KEY,
                    Name VARCHAR(100),
                    Department VARCHAR(100),
                    Salary INT
                )
            END
            """
        )

        connection.commit()

        # Insert new employees or update existing employees.
        merge_query = """
            MERGE dbo.Employees AS target
            USING
            (
                SELECT
                    ? AS EmployeeID,
                    ? AS Name,
                    ? AS Department,
                    ? AS Salary
            ) AS source
            ON target.EmployeeID = source.EmployeeID

            WHEN MATCHED THEN
                UPDATE SET
                    Name = source.Name,
                    Department = source.Department,
                    Salary = source.Salary

            WHEN NOT MATCHED THEN
                INSERT
                (
                    EmployeeID,
                    Name,
                    Department,
                    Salary
                )
                VALUES
                (
                    source.EmployeeID,
                    source.Name,
                    source.Department,
                    source.Salary
                );
        """

        required_columns = {
            "EmployeeID",
            "Name",
            "Department",
            "Salary"
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing columns in DataFrame: "
                f"{', '.join(sorted(missing_columns))}"
            )

        for _, row in df.iterrows():
            cursor.execute(
                merge_query,
                int(row["EmployeeID"]),
                str(row["Name"]),
                str(row["Department"]),
                int(row["Salary"])
            )

        connection.commit()

        print(
            "Transformed data loaded into Azure SQL successfully."
        )

    except Exception as error:
        if connection is not None:
            connection.rollback()

        print("Azure SQL loading failed:")
        print(error)

        # Important: send the error back to run_etl.py.
        raise

    finally:
        if connection is not None:
            connection.close()
            print("Azure SQL connection closed.")