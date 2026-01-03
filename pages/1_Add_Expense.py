import streamlit as st
import pandas as pd
from utils import load_data, save_data
from datetime import date

st.title("➕ Add New Expense")

df = load_data()

with st.form("expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Rent", "Utilities", "Entertainment", "Other"]
    )
    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
    description = st.text_input("Description")

    submit = st.form_submit_button("Add Expense")

    if submit:
        from utils import load_data, save_data, get_next_id

        new_row = {
            "ID": get_next_id(df),
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Description": description
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Expense added successfully ✅")
