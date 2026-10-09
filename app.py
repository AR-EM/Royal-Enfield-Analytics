import streamlit as st
from modules.utils import load_css, render_html
from modules.data_loader import load_data
from modules.filters import render_sidebar_filters, apply_filters
from modules.kpi_metrics import calculate_kpis, render_kpi_cards
from modules.charts import (
    plot_model_sales,
    plot_monthly_trend,
    plot_regional_sales,
    plot_customer_segments,
    plot_dealer_performance,
    plot_model_region_heatmap,
    plot_service_performance,
)

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Royal Enfield Business Performance Dashboard",
    page_icon="🏍️",
    layout="wide"
)

# ---------------------------------------------------------
# 2. LOAD EXTERNAL ASSETS (CSS STYLESHEET & HTML HEADER)
# ---------------------------------------------------------
load_css("assets/style.css")
render_html("assets/header.html")

# ---------------------------------------------------------
# 3. DATA INGESTION & PREPARATION (CACHED)
# ---------------------------------------------------------
df_master, df_service = load_data()

# ---------------------------------------------------------
# 4. SIDEBAR CROSS-FILTERS & EXECUTION
# ---------------------------------------------------------
filters = render_sidebar_filters(df_master)
filtered_sales, filtered_service = apply_filters(df_master, df_service, filters)

# ---------------------------------------------------------
# 5. KPI SUMMARY CARDS
# ---------------------------------------------------------
kpi_data = calculate_kpis(filtered_sales)
render_kpi_cards(kpi_data)

st.write("")

# ---------------------------------------------------------
# 6. ROW 1: SALES VOLUME & TREND
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Sales by Motorcycle Model")
        fig_model = plot_model_sales(filtered_sales)
        st.plotly_chart(fig_model, use_container_width=True)

with col2:
    with st.container(border=True):
        st.subheader("Monthly Sales Trend")
        fig_trend = plot_monthly_trend(filtered_sales)
        st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------
# 7. ROW 2: REGIONAL SALES & CUSTOMER SEGMENTS
# ---------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("Regional Sales")
        fig_reg = plot_regional_sales(filtered_sales)
        st.plotly_chart(fig_reg, use_container_width=True)

with col4:
    with st.container(border=True):
        st.subheader("Customer Segment Revenue")
        fig_donut = plot_customer_segments(filtered_sales, kpi_data['revenue_str'])
        st.plotly_chart(fig_donut, use_container_width=True)

# ---------------------------------------------------------
# 8. ROW 3: DEALER PERFORMANCE & HEATMAP
# ---------------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    with st.container(border=True):
        st.subheader("Dealer Performance — Top 10")
        fig_dealer = plot_dealer_performance(filtered_sales)
        st.plotly_chart(fig_dealer, use_container_width=True)

with col6:
    with st.container(border=True):
        st.subheader("Model × Region Heatmap")
        fig_heat = plot_model_region_heatmap(filtered_sales)
        if fig_heat is not None:
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.warning("No records match the current filter selection.")

# ---------------------------------------------------------
# 9. ROW 4: AFTER-SALES SERVICE DEMAND
# ---------------------------------------------------------
with st.container(border=True):
    st.subheader("Service Performance")
    st.caption("Which motorcycle models generate the highest after-sales service demand?")
    fig_serv = plot_service_performance(filtered_service)
    st.plotly_chart(fig_serv, use_container_width=True)

# ---------------------------------------------------------
# 10. EXTERNAL FOOTER HTML
# ---------------------------------------------------------
render_html("assets/footer.html")