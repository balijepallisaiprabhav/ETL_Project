from etl.extractor import extract_data
from etl.transformer import transform_data
from etl.loader import load_data
from etl.azure_loader import load_to_azure
from etl.logger_config import logger
from etl.emailer import send_email

def run_pipeline():
    try:
        logger.info("ETL pipeline started")

        data = extract_data()
        logger.info("Data extraction completed")

        transformed_data = transform_data(data)
        logger.info("Data transformation completed")

        load_data(transformed_data)
        logger.info("Data saved to CSV successfully")

        load_to_azure(transformed_data)
        logger.info("Data loaded into Azure SQL successfully")

        send_email()
        logger.info("Success email send")

        logger.info("ETL pipeline completed successfully")
        print("ETL pipeline completed successfully!")

    except Exception as error:
        logger.exception("ETL pipeline failed")
        print("ETL pipeline failed:")
        print(error)


if __name__ == "__main__":
    run_pipeline()