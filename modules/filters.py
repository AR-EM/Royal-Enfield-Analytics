import streamlit as st
import pandas as pd

def render_sidebar_filters(df_master: pd.DataFrame) -> dict:
    """
    Renders 6 interactive cross-filters in the Streamlit sidebar.
    Supports cascading dropdowns for State and Dealer based on selected Region/State.
    
    Parameters:
        df_master (pd.DataFrame): The merged master sales dataset.
        
    Returns:
        dict: A dictionary containing the user's filter selections.
    """
    st.sidebar.header("FILTERS")

    # 1. Region
    region_list = ['All Regions'] + sorted(df_master['Region'].dropna().unique().tolist())
    selected_region = st.sidebar.selectbox("Region", region_list)

    # 2. State (Cascades from Region)
    state_df = df_master if selected_region == 'All Regions' else df_master[df_master['Region'] == selected_region]
    state_list = ['All States'] + sorted(state_df['State'].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox("State", state_list)

    # 3. Motorcycle Model
    model_list = ['All Models'] + sorted(df_master['Model'].dropna().unique().tolist())
    selected_model = st.sidebar.selectbox("Motorcycle Model", model_list)

    # 4. Category
    category_list = ['All Categories'] + sorted(df_master['Category'].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Category", category_list)

    # 5. Dealer (Cascades from Region & State)
    dealer_df = df_master.copy()
    if selected_region != 'All Regions':
        dealer_df = dealer_df[dealer_df['Region'] == selected_region]
    if selected_state != 'All States':
        dealer_df = dealer_df[dealer_df['State'] == selected_state]
    dealer_options = ['All Dealers'] + sorted(dealer_df['Dealer_Name'].dropna().unique().tolist())
    selected_dealer = st.sidebar.selectbox("Dealer", dealer_options)

    # 6. Date / Month
    month_list = ['All Months'] + sorted(df_master['Year_Month'].unique().tolist())
    selected_month = st.sidebar.selectbox("Month", month_list)

    return {
        'region': selected_region,
        'state': selected_state,
        'model': selected_model,
        'category': selected_category,
        'dealer': selected_dealer,
        'month': selected_month
    }

def apply_filters(df_master: pd.DataFrame, df_service: pd.DataFrame, selected_filters: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Applies the selected filter criteria to the sales and service datasets.
    
    Parameters:
        df_master (pd.DataFrame): Master sales dataframe.
        df_service (pd.DataFrame): Master service dataframe.
        selected_filters (dict): Dictionary with selected filter values.
        
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (filtered_sales, filtered_service)
    """
    filtered_sales = df_master.copy()
    filtered_service = df_service.copy()

    if selected_filters['region'] != 'All Regions':
        filtered_sales = filtered_sales[filtered_sales['Region'] == selected_filters['region']]
        filtered_service = filtered_service[filtered_service['Region'] == selected_filters['region']]

    if selected_filters['state'] != 'All States':
        filtered_sales = filtered_sales[filtered_sales['State'] == selected_filters['state']]
        filtered_service = filtered_service[filtered_service['State'] == selected_filters['state']]

    if selected_filters['model'] != 'All Models':
        filtered_sales = filtered_sales[filtered_sales['Model'] == selected_filters['model']]
        filtered_service = filtered_service[filtered_service['Model'] == selected_filters['model']]

    if selected_filters['category'] != 'All Categories':
        filtered_sales = filtered_sales[filtered_sales['Category'] == selected_filters['category']]
        filtered_service = filtered_service[filtered_service['Category'] == selected_filters['category']]

    if selected_filters['dealer'] != 'All Dealers':
        filtered_sales = filtered_sales[filtered_sales['Dealer_Name'] == selected_filters['dealer']]
        filtered_service = filtered_service[filtered_service['Dealer_Name'] == selected_filters['dealer']]

    if selected_filters['month'] != 'All Months':
        filtered_sales = filtered_sales[filtered_sales['Year_Month'] == selected_filters['month']]

    return filtered_sales, filtered_service
