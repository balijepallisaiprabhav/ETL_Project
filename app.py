import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ETL Pipeline Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ETL Pipeline Dashboard")
st.subheader("Automated Data Extraction, Transformation & Loading")

st.success("ETL Pipeline Project")

st.markdown("""
This project automates the ETL process using Python,
Azure SQL Database, and GitHub Actions.
""")

st.header("Project Technologies")

col1, col2, col3 = st.columns(3)

col1.metric("Data Processing", "Python")
col2.metric("Database", "Azure SQL")
col3.metric("Automation", "GitHub Actions")

st.header("Pipeline Workflow")

st.write("""
1. Extract data
2. Transform data using Python
3. Load transformed data into Azure SQL Database
4. Automate execution using GitHub Actions
""")

st.header("Project Status")

st.success("GitHub Actions ETL workflow executed successfully ✅")

st.markdown("### GitHub Repository")
st.markdown(
    "[View Source Code](https://github.com/balijepallisaiprabhav/ETL_Project)"
)
