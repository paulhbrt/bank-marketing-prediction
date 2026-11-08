import streamlit as st
import pandas as pd

df = pd.read_csv("data/raw/bank-additional-full.csv")

total_clients = len(df)
subscribed_clients = df["deposit"].str.lower().eq("yes").sum()
subscription_rate = subscribed_clients / total_clients * 100
average_balance = df["balance"].mean()

st.title("Bank Marketing Analytics")

st.write(
    "Customer insights, campaign performance "
    "and predictive analytics."
)

st.divider()

st.subheader("Overview")

st.write("Key figures from the bank marketing dataset.")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total clients",
    f"{total_clients:,}".replace(",", " ")
)

col2.metric(
    "Subscription rate",
    f"{subscription_rate:.1f}%"
)

col3.metric(
    "Successful subscriptions",
    f"{subscribed_clients:,}".replace(",", " ")
)

col4.metric(
    "Average balance",
    f"{average_balance:,.0f}".replace(",", " ")
)

st.divider()

st.subheader("Subscription Distribution")

subscription_counts = (
    df["deposit"]
    .str.lower()
    .map({"yes": "Subscribed", "no": "Not subscribed"})
    .value_counts()
)

st.bar_chart(subscription_counts)