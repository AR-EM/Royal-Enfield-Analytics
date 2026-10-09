import streamlit as st
import pandas as pd

def calculate_kpis(filtered_sales: pd.DataFrame) -> dict:
    """
    Computes headline business KPIs from the filtered sales dataset.
    
    Parameters:
        filtered_sales (pd.DataFrame): Filtered sales records.
        
    Returns:
        dict: KPI values formatted for display.
    """
    total_revenue = filtered_sales['On_Road_Price'].sum()
    total_units = len(filtered_sales)
    avg_selling_price = (total_revenue / total_units) if total_units > 0 else 0
    total_dealers = filtered_sales['Dealer_ID'].nunique()
    total_customers = filtered_sales['Customer_ID'].nunique()
    avg_discount = filtered_sales['Discount_Amount'].mean() if total_units > 0 else 0

    revenue_str = f"₹{total_revenue / 1e7:.1f} Cr" if total_revenue >= 1e7 else f"₹{total_revenue:,.0f}"

    return {
        'total_revenue': total_revenue,
        'revenue_str': revenue_str,
        'total_units': total_units,
        'avg_selling_price': avg_selling_price,
        'total_dealers': total_dealers,
        'total_customers': total_customers,
        'avg_discount': avg_discount
    }

def render_kpi_cards(kpis: dict) -> None:
    """
    Renders 6 boxed KPI metric cards in a responsive horizontal grid.
    
    Parameters:
        kpis (dict): Precalculated KPI metrics dictionary.
    """
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        with st.container(border=True):
            st.metric("TOTAL REVENUE", kpis['revenue_str'])
    with k2:
        with st.container(border=True):
            st.metric("TOTAL BIKES SOLD", f"{kpis['total_units']:,}")
    with k3:
        with st.container(border=True):
            st.metric("AVG SELLING PRICE", f"₹{kpis['avg_selling_price']:,.0f}")
    with k4:
        with st.container(border=True):
            st.metric("TOTAL DEALERS", f"{kpis['total_dealers']:,}")
    with k5:
        with st.container(border=True):
            st.metric("TOTAL CUSTOMERS", f"{kpis['total_customers']:,}")
    with k6:
        with st.container(border=True):
            st.metric("AVG DISCOUNT", f"₹{kpis['avg_discount']:,.0f}")
