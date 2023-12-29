import streamlit as st
from st_pages import add_page_title
import requests
import pandas as pd
import hashlib


def post_transactions(account, df, checksum):
    transactions = []
    for t in df.to_dict(orient="records"):
        if "Id" in df.columns:
            id = t["Id"]
        else:
            id = f"{checksum}_{t['Date']}_{t['Description']}"
        transactions.append(
            {
                "id": id,
                "date": t["Date"],
                "description": t["Description"],
                "amount_c": int(float(t["Amount"].replace(",", "")) * 100),
                "account": account,
                "category": t["Category"] if "Category" in t else None,
            }
        )
    r = requests.post(
        "http://flask:5000/transactions",
        json={
            "account": account,
            "transactions": transactions,
        },
    )
    return r


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

# Get uploaded files

"Pick an Account:"
account = st.selectbox("", ["New"] + accounts)


# Upload a file
uploaded_file = st.file_uploader("Upload a statement (csv):")

if uploaded_file is not None:
    checksum = hashlib.md5(uploaded_file.getvalue()).hexdigest()
    if account == "New":
        account_name = st.text_input("Account Name")
        df = pd.read_csv(uploaded_file, header=None)
        # Add headers
        df.columns = [f"H{i}" for i in range(1, len(df.columns) + 1)]
        df
        # Set number of header rows
        num_header_rows = st.number_input(
            "Number of header rows", 0, 10, 1, help="Number of header rows"
        )
        # Let user pick column names
        col_names = []
        for col in df.columns:
            col_names.append(
                st.selectbox(
                    col,
                    [
                        col,
                        "Id",
                        "Date",
                        "Description",
                        "Amount",
                        "Category",
                        "Notes",
                    ],
                )
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
            df = df.iloc[num_header_rows:]
            df.columns = col_names
            df = df[[col for col in col_names if col[0] != "H"]]
            df
            if st.button(f"Add Account **{account_name}** and Import"):
                r = requests.post(
                    "http://flask:5000/account",
                    json={
                        "name": account_name,
                        "transaction_headers": col_names,
                        "header_rows": num_header_rows,
                    },
                )
                if r.status_code == 200:
                    st.success("Account added successfully")
                else:
                    st.error("Something went wrong")
                    st.write(r.text)
                post_transactions(account_name, df, checksum)
                uploaded_file = None
                st.experimental_rerun()

    else:
        st.write("Account:", account)
        df = pd.read_csv(uploaded_file, header=None)
        # Add headers
        df.columns = accounts_df.loc[
            accounts_df["name"] == account, "transaction_headers"
        ].iloc[0]
        df = df.iloc[
            accounts_df.loc[accounts_df["name"] == account, "header_rows"].iloc[0] :
        ]
        df
        if st.button("Import"):
            post_transactions(account, df, checksum)
            uploaded_file = None
            st.experimental_rerun()
