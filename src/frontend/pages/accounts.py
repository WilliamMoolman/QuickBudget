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

df = pd.DataFrame(transactions)[["name", "balance", "_id"]]
if len(df) > 0:
    df["balance"] = df["balance"].apply(
        lambda x: f"£{x/100 if x is not None else 0:,.2f}"
    )

# Page Display
if len(df) == 0:
    "No accounts found. Please upload a statement on the `Import` page."
    st.stop()


def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=True),
        },
        column_order=["Select", "name", "balance"],
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop("Select", axis=1)


selection = dataframe_with_selections(df)

if len(selection) == 0:
    st.stop()

if st.button("Delete Selected"):
    selection

    for account in selection["_id"].tolist():
        st.write(account)
        account

    r = requests.delete(f"http://flask:5000/account/{account}")
    if r.status_code == 200:
        st.success(f"Successfully deleted {account}")
        # st.stop()
    else:
        st.error(f"Failed to delete {account}")
        r.text
        # st.stop()

    st.experimental_rerun()
