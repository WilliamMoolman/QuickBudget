# Introduction
QuickBudget is meant to replace the now deprecated MoneyDashboard. The app is tailored towards what I personally used it for, however I plan on trying to replicate as much of the original functionality as possible.

# Architecture
QuickBudget will use Streamlit for frontend rendering (as I am not a frontend dev), and MongoDB for persistent storage. First prototype is single user, with login and authentication to be added later.

## Pages
- Import
    - Need to define headers for file. Bank specific?
- Export
- Accounts
- Rules
- Transactions
- Graphs
    - Year on Year
    - Monthly
- Budget
    - Set up monthly budget
