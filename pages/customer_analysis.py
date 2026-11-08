import streamlit as st
import pandas as pd

df = pd.read_csv("data/raw/bank-additional-full.csv")

df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 24, 34, 44, 54, 64, float("inf")],
    labels=["Under 25", "25-34", "35-44", "45-54", "55-64", "65+"]
)

st.title("Customer Analysis")

st.write(
    "Explore customer profiles and identify the characteristics "
    "associated with term deposit subscriptions."
)

st.divider()

st.sidebar.divider()
st.sidebar.subheader("Customer Filters")

jobs = ["All"] + sorted(df["job"].dropna().unique().tolist())
marital_statuses = ["All"] + sorted(df["marital"].dropna().unique().tolist())
educations = ["All"] + sorted(df["education"].dropna().unique().tolist())

selected_job = st.sidebar.selectbox("Profession", jobs)
selected_marital = st.sidebar.selectbox("Marital status", marital_statuses)
selected_education = st.sidebar.selectbox("Education", educations)

filtered_df = df.copy()

if selected_job != "All":
    filtered_df = filtered_df[filtered_df["job"] == selected_job]

if selected_marital != "All":
    filtered_df = filtered_df[filtered_df["marital"] == selected_marital]

if selected_education != "All":
    filtered_df = filtered_df[filtered_df["education"] == selected_education]

st.subheader("Customer Overview")

total_clients = len(filtered_df)

if total_clients > 0:
    subscribed_clients = filtered_df["deposit"].str.lower().eq("yes").sum()
    subscription_rate = subscribed_clients / total_clients * 100
    average_age = filtered_df["age"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Customers", f"{total_clients:,}".replace(",", " "))
    col2.metric("Subscription rate", f"{subscription_rate:.1f}%")
    col3.metric("Average age", f"{average_age:.1f} years")

    st.divider()

    st.subheader("Subscription Rate by Profession")

    job_rates = (
        filtered_df.groupby("job")["deposit"]
        .apply(lambda x: x.str.lower().eq("yes").mean() * 100)
        .sort_values(ascending=False)
        .to_frame("Subscription rate (%)")
    )

    st.bar_chart(job_rates)

    st.divider()

    st.subheader("Subscription Rate by Age Group")

    age_rates = (
        filtered_df.groupby("age_group", observed=True)["deposit"]
        .apply(lambda x: x.str.lower().eq("yes").mean() * 100)
        .to_frame("Subscription rate (%)")
    )

    st.bar_chart(age_rates)

else:
    st.warning("No customers match the selected filters.")