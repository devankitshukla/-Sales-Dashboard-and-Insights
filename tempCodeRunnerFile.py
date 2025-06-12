# superstore_dashboard.py

import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv('Sample - Superstore.csv', encoding='ISO-8859-1')

# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.strftime('%b')

st.set_page_config(layout='wide')
st.title("📊 Superstore Sales Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

df_selection = df[(df['Region'].isin(region)) & (df['Category'].isin(category))]

# KPI Cards
total_sales = int(df_selection['Sales'].sum())
total_profit = int(df_selection['Profit'].sum())
total_orders = df_selection['Order ID'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,}")
col2.metric("📈 Total Profit", f"${total_profit:,}")
col3.metric("📦 Total Orders", total_orders)

# Sales by Category
fig_category = px.bar(df_selection.groupby('Category')['Sales'].sum().reset_index(),
                      x='Category', y='Sales', title="Sales by Category", color='Category')
st.plotly_chart(fig_category, use_container_width=True)

# Sales Trend over Time
sales_trend = df_selection.groupby('Order Date')['Sales'].sum().reset_index()
fig_trend = px.line(sales_trend, x='Order Date', y='Sales', title='Sales Trend Over Time')
st.plotly_chart(fig_trend, use_container_width=True)

# Sales by State (Map)
fig_map = px.choropleth(df_selection,
                        locations='State',
                        locationmode='USA-states',
                        color='Sales',
                        scope='usa',
                        title='Sales by State')
# Optional: comment out if map doesn't render correctly
# st.plotly_chart(fig_map, use_container_width=True)

# Top Products
top_products = df_selection.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
st.subheader("🔝 Top 10 Products by Sales")
st.bar_chart(top_products)

st.markdown("---")
st.write("📌 **Insights:**")
st.markdown("""
- 🔻 High discount correlates with lower profits in some categories.
- 🛒 Technology outperforms in total profit despite fewer orders.
- 📉 Furniture has high returns but also higher losses in some regions.
""")
