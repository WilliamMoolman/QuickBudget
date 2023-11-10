# Main welcome page

import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
st.set_page_config(page_title="QuickBudget - Track your expenses and income", page_icon=":moneybag:")

# Setup the sidebar
show_pages(
    [
        Page("app.py", "Welcome", "🏠"),
        Page("pages/budget.py", "Budget", "📈"),
        Page("pages/accounts.py", "Accounts", "🏦"),
        Page("pages/transactions.py", "Transactions", "💸"),
        Page("pages/import.py", "Import", "📥"),
        Page("pages/export.py", "Export", "📤"),
        Page("pages/reports.py", "Reports", "📊"),
        Page("pages/rules.py", "Rules", "🔍"),
        Page("pages/settings.py", "Settings", "⚙️"),
    ]
)

# Page content
st.title("🏠 Welcome to QuickBudget!")
"""
Hello and welcome to QuickBudget! This is a simple budgeting app that allows you to track your expenses and income.

To get started, setup your accounts on the `Accounts` page. Then, import your transactions on the `Transactions` page.
"""
