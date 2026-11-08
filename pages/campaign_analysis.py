import streamlit as st
import pandas as pd

df = pd.read_csv("data/raw/bank-additional-full.csv")

month_order = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

st.title("Campaign Analysis")

st.write(
    "Analyze marketing campaign results across different "
    "periods and previous campaign outcomes."
)

st.divider()

st.sidebar.divider()
st.sidebar.subheader("Campaign Filters")

months = ["All"] + month_order
outcomes = ["All"] + sorted(df["poutcome"].dropna().unique().tolist())

selected_month = st.sidebar.selectbox("Contact month", months)
selected_outcome = st.sidebar.selectbox("Previous campaign outcome", outcomes)

filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["month"] == selected_month]

if selected_outcome != "All":
    filtered_df = filtered_df[filtered_df["poutcome"] == selected_outcome]

st.subheader("Campaign Overview")

total_contacts = len(filtered_df)

if total_contacts > 0:
    subscribed_clients = filtered_df["deposit"].str.lower().eq("yes").sum()
    subscription_rate = subscribed_clients / total_contacts * 100
    average_campaign_contacts = filtered_df["campaign"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total contacts", f"{total_contacts:,}".replace(",", " "))
    col2.metric("Subscription rate", f"{subscription_rate:.1f}%")
    col3.metric("Average contacts per client", f"{average_campaign_contacts:.1f}")

    st.divider()

    st.subheader("Monthly Campaign Performance")

    monthly_stats = (
        filtered_df.groupby("month")
        .agg(
            contacts=("deposit", "size"),
            subscriptions=("deposit", lambda x: x.str.lower().eq("yes").sum())
        )
        .reindex(month_order)
        .dropna()
    )

    monthly_stats["subscription_rate"] = (
        monthly_stats["subscriptions"] / monthly_stats["contacts"] * 100
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Number of contacts by month**")
        st.bar_chart(monthly_stats[["contacts"]])

    with col2:
        st.markdown("**Subscription rate by month**")
        st.bar_chart(monthly_stats[["subscription_rate"]])

    st.divider()

    st.subheader("Previous Campaign Outcome")

    outcome_stats = (
        filtered_df.groupby("poutcome")
        .agg(
            contacts=("deposit", "size"),
            subscriptions=("deposit", lambda x: x.str.lower().eq("yes").sum())
        )
    )

    outcome_stats["subscription_rate"] = (
        outcome_stats["subscriptions"] / outcome_stats["contacts"] * 100
    )

    st.bar_chart(outcome_stats[["subscription_rate"]])

    st.dataframe(
        outcome_stats.rename(
            columns={
                "contacts": "Contacts",
                "subscriptions": "Subscriptions",
                "subscription_rate": "Subscription rate (%)"
            }
        ).round(1),
        use_container_width=True
    )

else:
    st.warning("No campaign data matches the selected filters.")