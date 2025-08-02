import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💰 Expense Tracker")

# ---------- Session State to Hold Data ----------
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# ---------- Add Expense ----------
st.header("➕ Add New Expense")
with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.now())
        category = st.selectbox("Category", ['Food', 'Transport', 'Shopping', 'Utilities', 'Health', 'Other'])
    with col2:
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        desc = st.text_input("Description", placeholder="E.g., Groceries")

    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_data = pd.DataFrame([[date, category, amount, desc]], columns=st.session_state.df.columns)
        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
        st.success("Expense added!")

# ---------- Expense Table ----------
st.header("📋 Expense History")
st.dataframe(st.session_state.df, use_container_width=True)

# ---------- Analytics ----------
if not st.session_state.df.empty:
    st.header("📊 Analytics")

    # Monthly expenses
    df = st.session_state.df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)

    monthly_expense = df.groupby('Month')['Amount'].sum()
    st.subheader("Monthly Spending")
    st.bar_chart(monthly_expense)

    # Category-wise expenses
    category_expense = df.groupby('Category')['Amount'].sum()
    st.subheader("Spending by Category")
    fig, ax = plt.subplots()
    category_expense.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)
else:
    st.info("No expenses to analyze yet. Add some!")

