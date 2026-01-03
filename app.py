import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker Dashboard")

# Load data
df = load_data()

# Clean Date column
df["Date"] = pd.to_datetime(
    df["Date"].astype(str).str.strip(),
    errors="coerce"
)
df = df.dropna(subset=["Date"])

# Filters
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Date"].min(), df["Date"].max()]
)

filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# KPIs
st.metric("Total Expense", f"₹ {filtered_df['Amount'].sum()}")

# Charts
st.subheader("📊 Expense Analysis")

col1, col2 = st.columns(2)

with col1:
    pie_data = filtered_df.groupby("Category")["Amount"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
    st.pyplot(fig1)

with col2:
    line_data = filtered_df.groupby("Date")["Amount"].sum()
    fig2, ax2 = plt.subplots()
    ax2.plot(line_data.index, line_data.values)
    st.pyplot(fig2)

# Table
st.subheader("📄 Expense Records")
st.dataframe(filtered_df)

st.subheader("🗑️ Delete Expense")

# Select expense by ID
expense_ids = filtered_df["ID"].tolist()

if expense_ids:
    selected_id = st.selectbox("Select Expense ID to delete", expense_ids)

    if st.button("Delete Selected Expense"):
        df = df[df["ID"] != selected_id]
        from utils import save_data
        save_data(df)
        st.success(f"Expense ID {selected_id} deleted successfully ✅")
        st.rerun()
else:
    st.info("No expenses available to delete.")

st.subheader("✏️ Update Expense")

expense_ids = df["ID"].tolist()

if expense_ids:
    selected_id = st.selectbox("Select Expense ID to update", expense_ids)

    # Get selected expense
    selected_row = df[df["ID"] == selected_id].iloc[0]

    with st.form("update_form"):
        updated_date = st.date_input(
            "Date",
            pd.to_datetime(selected_row["Date"])
        )
        updated_category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping", "Rent", "Utilities", "Entertainment", "Other"],
            index=["Food", "Travel", "Shopping", "Rent", "Utilities", "Entertainment", "Other"].index(selected_row["Category"])
        )
        updated_amount = st.number_input(
            "Amount (₹)",
            value=float(selected_row["Amount"]),
            min_value=0.0
        )
        updated_description = st.text_input(
            "Description",
            value=selected_row["Description"]
        )

        update_btn = st.form_submit_button("Update Expense")

        if update_btn:
            df.loc[df["ID"] == selected_id, "Date"] = updated_date.strftime("%Y-%m-%d")
            df.loc[df["ID"] == selected_id, "Category"] = updated_category
            df.loc[df["ID"] == selected_id, "Amount"] = updated_amount
            df.loc[df["ID"] == selected_id, "Description"] = updated_description

            from utils import save_data
            save_data(df)

            st.success("Expense updated successfully ✅")
            st.rerun()
else:
    st.info("No expenses available to update.")
