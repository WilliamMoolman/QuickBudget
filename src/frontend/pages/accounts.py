import streamlit as st
import requests
import st_pages
import pandas as pd

# Set config
st.set_page_config(
    page_title="QuickBudget - Track your expenses and income",
    page_icon=":moneybag:",
    layout="wide",
)
st_pages.add_page_title()

# Fetching data
transactions = requests.get("http://flask:5000/accounts").json()

df = pd.DataFrame(transactions)
if len(df) > 0:
    df["balance"] = df["balance"].apply(
        lambda x: f"£{x/100 if x is not None else 0:,.2f}"
    )

# Page Display
if len(df) > 0:
    df
else:
    "No accounts found. Please upload a statement on the `Import` page."
