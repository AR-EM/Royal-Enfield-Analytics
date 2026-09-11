import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & MINIMAL CARD STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Royal Enfield Business Performance Dashboard",
    page_icon="",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        /* Compact KPI Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            color: #6b7280 !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            white-space: nowrap !important;
        }
        /* Tighten metric padding within bordered containers */
        [data-testid="stMetric"] {
            padding: 0.2rem 0 !important;
        }
        /* Header spacing */
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("ROYAL ENFIELD BUSINESS PERFORMANCE DASHBOARD")
st.caption("Sales • Customers • Dealers • Service — Performance Analytics")
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATA INGESTION & PREPARATION (CACHED)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    sales = pd.read_csv('Sales.csv')
    dealers = pd.read_csv('Dealers.csv')
    customers = pd.read_csv('Customers.csv')
    motorcycles = pd.read_csv('Motorcycles.csv')
    service = pd.read_csv('Service.csv')

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

df_master, df_service = load_data()

# ---------------------------------------------------------
# 3. SIDEBAR FILTERS (6 CROSS-FILTERS)
# ---------------------------------------------------------
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

# 5. Dealer
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

# ---------------------------------------------------------
# 4. FILTER EXECUTION
# ---------------------------------------------------------
filtered_sales = df_master.copy()
filtered_service = df_service.copy()

if selected_region != 'All Regions':
    filtered_sales = filtered_sales[filtered_sales['Region'] == selected_region]
    filtered_service = filtered_service[filtered_service['Region'] == selected_region]

if selected_state != 'All States':
    filtered_sales = filtered_sales[filtered_sales['State'] == selected_state]
    filtered_service = filtered_service[filtered_service['State'] == selected_state]

if selected_model != 'All Models':
    filtered_sales = filtered_sales[filtered_sales['Model'] == selected_model]
    filtered_service = filtered_service[filtered_service['Model'] == selected_model]

if selected_category != 'All Categories':
    filtered_sales = filtered_sales[filtered_sales['Category'] == selected_category]
    filtered_service = filtered_service[filtered_service['Category'] == selected_category]

if selected_dealer != 'All Dealers':
    filtered_sales = filtered_sales[filtered_sales['Dealer_Name'] == selected_dealer]
    filtered_service = filtered_service[filtered_service['Dealer_Name'] == selected_dealer]

if selected_month != 'All Months':
    filtered_sales = filtered_sales[filtered_sales['Year_Month'] == selected_month]

# ---------------------------------------------------------
# 5. KPI CARDS (BOXED & AUTO-SIZED)
# ---------------------------------------------------------
total_revenue = filtered_sales['On_Road_Price'].sum()
total_units = len(filtered_sales)
avg_selling_price = (total_revenue / total_units) if total_units > 0 else 0
total_dealers = filtered_sales['Dealer_ID'].nunique()
total_customers = filtered_sales['Customer_ID'].nunique()
avg_discount = filtered_sales['Discount_Amount'].mean() if total_units > 0 else 0

revenue_str = f"₹{total_revenue / 1e7:.1f} Cr" if total_revenue >= 1e7 else f"₹{total_revenue:,.0f}"

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    with st.container(border=True):
        st.metric("TOTAL REVENUE", revenue_str)
with k2:
    with st.container(border=True):
        st.metric("TOTAL BIKES SOLD", f"{total_units:,}")
with k3:
    with st.container(border=True):
        st.metric("AVG SELLING PRICE", f"₹{avg_selling_price:,.0f}")
with k4:
    with st.container(border=True):
        st.metric("TOTAL DEALERS", f"{total_dealers:,}")
with k5:
    with st.container(border=True):
        st.metric("TOTAL CUSTOMERS", f"{total_customers:,}")
with k6:
    with st.container(border=True):
        st.metric("AVG DISCOUNT", f"₹{avg_discount:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. ROW 1: SALES VOLUME & TREND
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Sales by Motorcycle Model")
        model_vol = filtered_sales['Model'].value_counts().reset_index()
        model_vol.columns = ['Model', 'Units_Sold']
        
        fig_model = px.bar(
            model_vol, x='Model', y='Units_Sold',
            text='Units_Sold', color_discrete_sequence=['#1f77b4']
        )
        fig_model.update_traces(textposition='outside', cliponaxis=False)
        fig_model.update_layout(
            height=400,
            xaxis=dict(tickangle=-45, automargin=True, title=None),
            yaxis=dict(automargin=True, title="Units Sold"),
            margin=dict(l=30, r=20, t=30, b=80)
        )
        st.plotly_chart(fig_model, use_container_width=True)

with col2:
    with st.container(border=True):
        st.subheader("Monthly Sales Trend")
        trend = filtered_sales.groupby('Year_Month')['Sale_ID'].count().reset_index(name='Units_Sold')
        trend = trend.sort_values('Year_Month')
        
        fig_trend = px.line(
            trend, x='Year_Month', y='Units_Sold',
            markers=True, line_shape='spline', color_discrete_sequence=['#1f77b4']
        )
        fig_trend.update_layout(
            height=400,
            xaxis=dict(tickangle=-45, automargin=True, title=None),
            yaxis=dict(automargin=True, title="Units Sold"),
            margin=dict(l=30, r=20, t=30, b=60)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------
# 7. ROW 2: REGIONAL SALES & CUSTOMER SEGMENTS
# ---------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("Regional Sales")
        region_rev = filtered_sales.groupby('Region')['On_Road_Price'].sum().reset_index(name='Revenue')
        region_rev['Revenue_Cr'] = region_rev['Revenue'] / 1e7
        region_rev = region_rev.sort_values(by='Revenue', ascending=False)
        
        fig_reg = px.bar(
            region_rev, x='Region', y='Revenue_Cr',
            text=region_rev['Revenue_Cr'].apply(lambda x: f"₹{x:.1f} Cr"),
            color_discrete_sequence=['#e65c00']
        )
        fig_reg.update_traces(textposition='outside', cliponaxis=False)
        fig_reg.update_layout(
            height=390,
            xaxis=dict(automargin=True, title=None),
            yaxis=dict(automargin=True, title="Revenue (₹ Cr)"),
            margin=dict(l=30, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_reg, use_container_width=True)

with col4:
    with st.container(border=True):
        st.subheader("Customer Segment Revenue")
        seg_rev = filtered_sales.groupby('Customer_Segment')['On_Road_Price'].sum().reset_index(name='Revenue')
        
        fig_donut = px.pie(
            seg_rev, names='Customer_Segment', values='Revenue',
            hole=0.52, color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.add_annotation(
            text=f"<b>{revenue_str}</b><br><span style='font-size:11px; color:gray;'>Total</span>",
            showarrow=False, font_size=14
        )
        fig_donut.update_layout(
            height=390,
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# ---------------------------------------------------------
# 8. ROW 3: DEALER PERFORMANCE & HEATMAP
# ---------------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    with st.container(border=True):
        st.subheader("Dealer Performance — Top 10")
        dealer_perf = filtered_sales.groupby('Dealer_Name')['On_Road_Price'].sum().reset_index(name='Revenue')
        dealer_perf['Revenue_Cr'] = dealer_perf['Revenue'] / 1e7
        dealer_perf = dealer_perf.sort_values(by='Revenue', ascending=False).head(10)
        
        fig_dealer = px.bar(
            dealer_perf, x='Revenue_Cr', y='Dealer_Name',
            orientation='h',
            text=dealer_perf['Revenue_Cr'].apply(lambda x: f"₹{x:.2f} Cr"),
            color_discrete_sequence=['#00a86b']
        )
        fig_dealer.update_traces(textposition='outside', cliponaxis=False)
        fig_dealer.update_layout(
            height=430,
            yaxis=dict(autorange="reversed", automargin=True, title=None),
            xaxis=dict(automargin=True, title="Revenue (₹ Cr)"),
            margin=dict(l=20, r=60, t=20, b=40)
        )
        st.plotly_chart(fig_dealer, use_container_width=True)

with col6:
    with st.container(border=True):
        st.subheader("Model × Region Heatmap")
        if not filtered_sales.empty:
            grid = pd.crosstab(filtered_sales['Model'], filtered_sales['Region'])
            fig_heat = px.imshow(
                grid, text_auto=True, aspect="auto",
                color_continuous_scale='Blues'
            )
            fig_heat.update_layout(
                height=430,
                xaxis=dict(automargin=True, title=None),
                yaxis=dict(automargin=True, title=None),
                margin=dict(l=20, r=20, t=20, b=40)
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.warning("No records match the current filter selection.")

# ---------------------------------------------------------
# 9. ROW 4: AFTER-SALES SERVICE DEMAND (FIXED TEXT CUTOFF)
# ---------------------------------------------------------
with st.container(border=True):
    st.subheader("Service Performance")
    st.caption("Which motorcycle models generate the highest after-sales service demand?")

    serv_vol = filtered_service['Model'].value_counts().reset_index()
    serv_vol.columns = ['Model', 'Service_Count']

    fig_serv = px.bar(
        serv_vol, x='Model', y='Service_Count',
        text='Service_Count', color_discrete_sequence=['#4c3c92']
    )
    fig_serv.update_traces(textposition='outside', cliponaxis=False)
    fig_serv.update_layout(
        height=400,
        xaxis=dict(tickangle=-45, automargin=True, title=None),
        yaxis=dict(automargin=True, title="Service Records"),
        margin=dict(l=30, r=20, t=30, b=100)
    )
    st.plotly_chart(fig_serv, use_container_width=True)