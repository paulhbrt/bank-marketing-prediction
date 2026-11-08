import streamlit as st

st.set_page_config(
    page_title="Bank Marketing Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FA;
    color: #17243A;
}

[data-testid="stHeader"] {
    background-color: #F5F7FA;
}

[data-testid="stSidebar"] {
    background-color: #17243A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #17243A;
    font-weight: 600;
}

p {
    color: #64748B;
    font-size: 15px;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E5EAF0;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

overview = st.Page(
    "pages/overview.py",
    title="Overview",
    icon=":material/dashboard:",
    default=True
)

customer_analysis = st.Page(
    "pages/customer_analysis.py",
    title="Customer Analysis",
    icon=":material/groups:"
)

campaign_analysis = st.Page(
    "pages/campaign_analysis.py",
    title="Campaign Analysis",
    icon=":material/campaign:"
)

model_performance = st.Page(
    "pages/model_performance.py",
    title="Model Performance",
    icon=":material/monitoring:"
)

predictions = st.Page(
    "pages/predictions.py",
    title="Predictions",
    icon=":material/online_prediction:"
)

navigation = st.navigation({
    "ANALYTICS": [
        overview,
        customer_analysis,
        campaign_analysis
    ],
    "MACHINE LEARNING": [
        model_performance,
        predictions
    ]
})

st.sidebar.title("BANK MARKETING")
st.sidebar.caption("ANALYTICS PLATFORM")

navigation.run()
