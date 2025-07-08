
# Import necessary Libraries
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Load the cleaned dataset
df = pd.read_csv('cleaned_VGsales.csv')

st.title(" Video Game Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
Game = st.sidebar.multiselect("Select Game(s)", df['name'].unique())
platforms = st.sidebar.multiselect("Select Platform(s)", df['platform'].unique())
genres = st.sidebar.multiselect("Select Genre(s)", df['genre'].unique())
publishers = st.sidebar.multiselect("Select Publisher(s)", df['publisher'].unique())
year_range = st.sidebar.slider("Select Year Range", 
                               int(df['year'].min()), 
                               int(df['year'].max()), 
                               (int(df['year'].min()), int(df['year'].max())))

# Apply filters
filtered_df = df.copy()

if Game:
    filtered_df = filtered_df[filtered_df['name'].isin(Game)]

if platforms:
    filtered_df = filtered_df[filtered_df['platform'].isin(platforms)]

if genres:
    filtered_df = filtered_df[filtered_df['genre'].isin(genres)]

if publishers:
    filtered_df = filtered_df[filtered_df['publisher'].isin(publishers)]

filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]

# Visualizations
st.subheader("Data Table")
st.dataframe(filtered_df.head(50))

st.subheader("Top 10 Best-Selling Games")
top_games = filtered_df.sort_values(by="global_sales", ascending=False).head(10)
fig = px.bar(top_games, x="name", y="global_sales", title="Top 10 Games by Global Sales", labels={'global_sales': 'Global Sales (in millions)'})
st.plotly_chart(fig)

st.subheader("Sales Distribution by Region")
region_cols = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
region_sums = filtered_df[region_cols].sum().reset_index()
region_sums.columns = ['Region', 'Sales']
fig2 = px.pie(region_sums, names='Region', values='Sales', title="Regional Sales Distribution")
st.plotly_chart(fig2)

st.subheader("Game Sales Over the Years")
sales_by_year = filtered_df.groupby('year')['global_sales'].sum().reset_index()
fig3 = px.line(sales_by_year, x='year', y='global_sales', title="Total Global Sales by Year", labels={'global_sales': 'Global Sales'})
st.plotly_chart(fig3)

st.subheader("Relationship Between Platform, Genre, and Global Sales")
grouped = filtered_df.groupby(['platform', 'genre'])['global_sales'].sum().reset_index()
fig4 = px.bar(grouped.sort_values(by='global_sales', ascending=False).head(40),
             x='platform',
             y='global_sales',
             color='genre',
             title='Top Platform-Genre Combinations by Global Sales',
             labels={'global_sales': 'Global Sales (in millions)'})
st.plotly_chart(fig4)

