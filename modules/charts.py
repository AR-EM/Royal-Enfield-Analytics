import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_model_sales(filtered_sales: pd.DataFrame) -> go.Figure:
    """Generates a bar chart showing units sold by motorcycle model."""
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
    return fig_model

def plot_monthly_trend(filtered_sales: pd.DataFrame) -> go.Figure:
    """Generates a spline line chart displaying monthly sales volume trend."""
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
    return fig_trend

def plot_regional_sales(filtered_sales: pd.DataFrame) -> go.Figure:
    """Generates a bar chart showing revenue generated across regions in ₹ Crores."""
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
    return fig_reg

def plot_customer_segments(filtered_sales: pd.DataFrame, revenue_str: str) -> go.Figure:
    """Generates a donut chart displaying revenue contribution by customer segment."""
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
    return fig_donut

def plot_dealer_performance(filtered_sales: pd.DataFrame) -> go.Figure:
    """Generates a horizontal bar chart displaying top 10 dealers by revenue."""
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
    return fig_dealer

def plot_model_region_heatmap(filtered_sales: pd.DataFrame) -> go.Figure | None:
    """Generates a heatmap of motorcycle model sales counts across geographic regions."""
    if filtered_sales.empty:
        return None

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
    return fig_heat

def plot_service_performance(filtered_service: pd.DataFrame) -> go.Figure:
    """Generates a bar chart showing after-sales service demand across motorcycle models."""
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
    return fig_serv
