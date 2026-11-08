import streamlit as st
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv("data/raw/bank-additional-full.csv")
model = joblib.load("models/random_forest.pkl")

X = df.drop(columns=["deposit", "duration"])
y = df["deposit"].str.lower()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

probabilities = model.predict_proba(X_test)
yes_index = list(model.classes_).index("yes")
yes_probabilities = probabilities[:, yes_index]

st.title("Model Performance")

st.write(
    "Evaluate the Random Forest model and explore "
    "the impact of the prediction threshold."
)

st.divider()

st.subheader("Prediction Settings")

threshold = st.slider(
    "Prediction threshold",
    min_value=0.1,
    max_value=0.9,
    value=0.4,
    step=0.05
)

predictions = np.where(
    yes_probabilities >= threshold,
    "yes",
    "no"
)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, pos_label="yes", zero_division=0)
recall = recall_score(y_test, predictions, pos_label="yes", zero_division=0)
f1 = f1_score(y_test, predictions, pos_label="yes", zero_division=0)

st.divider()

st.subheader("Evaluation Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", f"{accuracy:.1%}")
col2.metric("Precision", f"{precision:.1%}")
col3.metric("Recall", f"{recall:.1%}")
col4.metric("F1-score", f"{f1:.1%}")

st.divider()

st.subheader("Confusion Matrix")

matrix = confusion_matrix(
    y_test,
    predictions,
    labels=["no", "yes"]
)

matrix_df = pd.DataFrame(
    matrix,
    index=["Actual: No", "Actual: Yes"],
    columns=["Predicted: No", "Predicted: Yes"]
)

st.dataframe(matrix_df, use_container_width=True)

st.divider()

st.subheader("Understanding the Metrics")

st.markdown("""
- **Accuracy:** proportion of all predictions that are correct.
- **Precision:** proportion of predicted subscriptions that are actually successful.
- **Recall:** proportion of actual subscriptions correctly identified by the model.
- **F1-score:** balance between precision and recall.
""")

st.write(
    f"With a threshold of {threshold:.2f}, "
    f"the model predicts {np.sum(predictions == 'yes'):,} "
    "potential subscriptions on the test dataset."
)