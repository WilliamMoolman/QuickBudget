import requests
import pandas as pd
import streamlit as st
import st_pages

# Set config
st.set_page_config(page_title="QuickBudget - Track your expenses and income", page_icon=":moneybag:", layout="wide")
st_pages.add_page_title()


# Fetching data
transactions = requests.get('http://flask:5000/transactions').json()

df = pd.DataFrame(transactions)

df["amount"] = df['amount_c'].apply(lambda x: f'£{x/100:,.2f}')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Filtering data
st.sidebar.title("Filter")
filter_type = st.sidebar.radio('Filter Type', ['Month', 'Year', 'None'])
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
month = st.sidebar.selectbox('Month', months, disabled=filter_type != 'Month')
year = st.sidebar.number_input('Year', 1900, 2100, 2021, disabled=filter_type == 'None')

if filter_type == 'None':
    filtered_df = df
elif filter_type == 'Month':
    filtered_df = df[(df['date'].dt.month == months.index(month)+1) & (df['date'].dt.year == year)]
else:
    filtered_df = df[df['date'].dt.year == year]

display_df = filtered_df[['date','description','amount','account','category','notes']]


# Page Display
display_df
