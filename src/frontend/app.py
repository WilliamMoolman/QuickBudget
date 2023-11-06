# Main welcome page

import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
st.set_page_config(page_title="QuickBudget - Track your expenses and income", page_icon=":moneybag:")

# Setup the sidebar
show_pages(
    [
        Page("app.py", "Welcome", "🏠"),
        Page("pages/budget.py", "Budget", ":chart_with_upwards_trend:"),
        Page("pages/accounts.py", "Accounts", ":bank:"),
        Page("pages/transactions.py", "Transactions", ":money_with_wings:"),
        Page("pages/import.py", "Import", ":inbox_tray:"),
        Page("pages/export.py", "Export", ":outbox_tray:"),
        Page("pages/reports.py", "Reports", ":bar_chart:"),
        Page("pages/rules.py", "Rules", ":mag:"),
        Page("pages/settings.py", "Settings", ":gear:"),
    ]
)

# Page content
st.title("🏠 Welcome to QuickBudget!")
"""
Hello and welcome to QuickBudget! This is a simple budgeting app that allows you to track your expenses and income.

To get started, setup your accounts on the `Accounts` page. Then, import your transactions on the `Transactions` page.
"""
