from pathlib import Path
import streamlit as st
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

@st.cache_data
def load_data():
    """
    Loads Sales, Dealers, Customers, Motorcycles, and Service CSVs,
    parses dates, formats Year_Month, and joins them into master DataFrames.
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (df_master, df_service)
    """
    sales = pd.read_csv(BASE_DIR / 'Sales.csv')
    dealers = pd.read_csv(BASE_DIR / 'Dealers.csv')
    customers = pd.read_csv(BASE_DIR / 'Customers.csv')
    motorcycles = pd.read_csv(BASE_DIR / 'Motorcycles.csv')
    service = pd.read_csv(BASE_DIR / 'Service.csv')

    # Parse Dates
    sales['Sale_Date'] = pd.to_datetime(sales['Sale_Date'])
    sales['Year_Month'] = sales['Sale_Date'].dt.to_period('M').astype(str)
    service['Service_Date'] = pd.to_datetime(service['Service_Date'])

    # Master Merges
    df = sales.merge(dealers, on='Dealer_ID', how='inner', suffixes=('', '_dealer'))
    df = df.merge(motorcycles, on='Bike_ID', how='inner', suffixes=('', '_bike'))
    df = df.merge(customers, on='Customer_ID', how='inner', suffixes=('', '_cust'))

    df_serv = service.merge(motorcycles, on='Bike_ID', how='inner')
    df_serv = df_serv.merge(dealers, on='Dealer_ID', how='inner')

    return df, df_serv
