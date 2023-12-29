import requests
import pandas as pd
import streamlit as st
import st_pages

# Set config
st.set_page_config(
    page_title="QuickBudget - Track your expenses and income",
    page_icon=":moneybag:",
    layout="wide",
)
st_pages.add_page_title()


# Fetching data
transactions = requests.get("http://flask:5000/transactions").json()

df = pd.DataFrame(transactions)

if len(df) == 0:
    st.write("No transactions found. Please upload a statement on the `Import` page.")
    st.stop()

df["amount"] = df["amount_c"].apply(lambda x: f"£{x/100:,.2f}")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Filtering data
st.sidebar.title("Filter")
st.sidebar.subheader("Time filter")
filter_type = st.sidebar.radio(
    "Filter Type",
    [
        "None",
        "Month",
        "Year",
    ],
)
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
month = st.sidebar.selectbox("Month", months, disabled=filter_type != "Month")
year = st.sidebar.number_input("Year", 1900, 2100, 2021, disabled=filter_type == "None")

st.sidebar.subheader("Account filter")
account = st.sidebar.selectbox(
    "Account", ["All"] + sorted(df["account"].unique()), index=0
)

if filter_type == "None":
    filtered_df = df
elif filter_type == "Month":
    filtered_df = df[
        (df["date"].dt.month == months.index(month) + 1) & (df["date"].dt.year == year)
    ]
else:
    filtered_df = df[df["date"].dt.year == year]

if account != "All":
    filtered_df = filtered_df[filtered_df["account"] == account]

display_df = filtered_df[
    ["date", "description", "amount", "account", "category", "notes"]
]


# Page Display
st.dataframe(display_df, use_container_width=True)
