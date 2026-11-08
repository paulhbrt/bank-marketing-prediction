import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load("models/random_forest.pkl")

st.title("Customer Predictions")

st.write(
    "Upload customer data to estimate their probability "
    "of subscribing to a term deposit."
)

st.divider()

st.subheader("Upload Customer Data")

uploaded_file = st.file_uploader(
    "Select a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    new_clients = pd.read_csv(uploaded_file)

    st.write(f"{len(new_clients)} customers loaded.")

    expected_features = list(model.feature_names_in_)

    prediction_data = new_clients.drop(
        columns=["deposit", "duration"],
        errors="ignore"
    )

    missing_features = [
        feature for feature in expected_features
        if feature not in prediction_data.columns
    ]

    if missing_features:
        st.error(
            f"Missing required features: {', '.join(missing_features)}"
        )

    else:

        prediction_data = prediction_data[expected_features]

        threshold = st.slider(
            "Prediction threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.4,
            step=0.05
        )

        probabilities = model.predict_proba(prediction_data)

        yes_index = list(model.classes_).index("yes")

        subscription_probabilities = probabilities[:, yes_index]

        predictions = np.where(
            subscription_probabilities >= threshold,
            "yes",
            "no"
        )

        results = new_clients.copy()

        results["subscription_probability"] = subscription_probabilities
        results["prediction"] = predictions

        results = results.sort_values(
            "subscription_probability",
            ascending=False
        )

        st.divider()

        st.subheader("Prediction Results")

        total_clients = len(results)
        potential_clients = (results["prediction"] == "yes").sum()
        average_probability = results["subscription_probability"].mean() * 100

        col1, col2, col3 = st.columns(3)

        col1.metric("Customers analyzed", f"{total_clients:,}")
        col2.metric("Potential subscribers", f"{potential_clients:,}")
        col3.metric("Average probability", f"{average_probability:.1f}%")

        st.divider()

        st.subheader("Customer Ranking")

        display_results = results.copy()
        display_results["subscription_probability"] = (
            display_results["subscription_probability"] * 100
        )

        st.dataframe(
            display_results,
            use_container_width=True
        )

        csv = results.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download predictions",
            data=csv,
            file_name="bank_marketing_predictions.csv",
            mime="text/csv"
        )

else:
    st.info("Upload a customer CSV file to generate predictions.")