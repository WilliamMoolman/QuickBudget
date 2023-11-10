import streamlit as st
from st_pages import add_page_title
import requests
import pandas as pd

# Set config
st.set_page_config(
    page_title="QuickBudget - Track your expenses and income",
    page_icon=":moneybag:",
    layout="wide",
)
add_page_title()

# Fetching data
accounts = requests.get("http://flask:5000/accounts").json()
accounts_df = pd.DataFrame(accounts)

if len(accounts) > 0:
    accounts = accounts_df["name"].tolist()
else:
    accounts = []


"Pick an Account:"
account = st.selectbox("", ["New"] + accounts)

# if account == 'New':
#     account = st.text_input('Account Name')
#     if st.button('Add Account'):
#         requests.post('http://flask:5000/account', json={'name': account})
#         st.experimental_rerun()

# Upload a file
uploaded_file = st.file_uploader("Upload a statement (csv):")

if uploaded_file is not None:
    if account == "New":
        account_name = st.text_input("Account Name")
        df = pd.read_csv(uploaded_file, header=None)
        # Add headers
        df.columns = [f"H{i}" for i in range(1, len(df.columns) + 1)]
        df
        # Let user pick column names
        col_names = []
        for col in df.columns:
            col_names.append(
                st.selectbox(col, ["None", "Date", "Description", "Amount", "Category"])
            )
        # Check if required columns are present
        if account_name == "":
            st.write("Please enter an account name")
        elif (
            "Date" not in col_names
            or "Amount" not in col_names
            or "Description" not in col_names
        ):
            st.write("Please select a column for Date, Amount and Description")
        else:
            if st.button(f"Add Account **{account_name}**"):
                r = requests.post(
                    "http://flask:5000/account",
                    json={"name": account_name, "transaction_headers": col_names},
                )
                if r.status_code == 200:
                    st.success("Account added successfully")
                else:
                    st.error("Something went wrong")
                    st.write(r.text)
                r = requests.post(
                    "http://flask:5000/transactions",
                    json={
                        "account": account_name,
                        "transactions": df.to_dict(orient="records"),
                    },
                )
                if r.status_code == 200:
                    st.success("Transactions added successfully")
                else:
                    st.error("Something went wrong")
                    st.write(r.text)
                uploaded_file = None
                st.experimental_rerun()
    else:
        st.write("Account:", account)
        df = pd.read_csv(uploaded_file, header=None)
        # Add headers
        df.columns = accounts_df.loc[
            accounts_df["name"] == account, "transaction_headers"
        ].iloc[0]
        df
        transactions = []
        for t in df.to_dict(orient="records"):
            transactions.append(
                {
                    "date": t["Date"],
                    "description": t["Description"],
                    "amount_c": int(float(t["Amount"].replace(",", "")) * 100),
                    "account": account,
                    "category": t["Category"] if "Category" in t else None,
                }
            )
        if st.button("Import"):
            r = requests.post(
                "http://flask:5000/transactions",
                json={
                    "account": account,
                    "transactions": transactions,
                },
            )
            if r.status_code == 200:
                st.success("Transactions added successfully")
                st.experimental_rerun()
            else:
                st.error("Something went wrong")
                st.write(r.text)
            uploaded_file = None
