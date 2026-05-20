import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="BIKE SALES PROFIT PREDICTOR",
    page_icon="📊",
    layout="wide"
)

# ---------------- CLEAN PROFESSIONAL CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

.stButton>button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    transform: none;
}

.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #1f2937;
}

.title {
    text-align: center;
    font-size: 48px !important;
    font-weight: 700;
    color: #e5e7eb;
    margin-top: 10px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = joblib.load("bike_sales_model.pkl")

# ---------------- SESSION STATE INIT ----------------

def reset_fields():
    st.session_state.age = 25
    st.session_state.gender = "M"
    st.session_state.country = "United States"
    st.session_state.category = "Accessories"
    st.session_state.qty = 1
    st.session_state.cost = 100.0
    st.session_state.price = 150.0

if "age" not in st.session_state:
    reset_fields()

# ---------------- HEADER ----------------

st.markdown('<p class="title">BIKE SALES PROFIT PREDICTOR</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Machine Learning Business Intelligence Dashboard</p>', unsafe_allow_html=True)

st.divider()

# ---------------- RESET BUTTON ----------------

col_reset, _ = st.columns([1, 5])

with col_reset:
    if st.button("Reset All Inputs"):
        reset_fields()
        st.rerun()

st.divider()

# ---------------- LAYOUT ----------------

left, right = st.columns(2)

# ---------------- INPUTS LEFT ----------------

with left:
    st.subheader("Customer Information")

    customer_age = st.slider("Customer Age", 10, 100, key="age")

    customer_gender = st.radio(
        "Customer Gender",
        ["M", "F"],
        horizontal=True,
        key="gender"
    )

    country = st.selectbox(
        "Country",
        ["United States", "United Kingdom", "Germany", "France", "Canada", "Australia"],
        key="country"
    )

    product_category = st.selectbox(
        "Product Category",
        ["Accessories", "Bikes", "Clothing"],
        key="category"
    )

# ---------------- INPUTS RIGHT ----------------

with right:
    st.subheader("Sales Information")

    order_quantity = st.number_input("Order Quantity", min_value=1, key="qty")

    unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, key="cost")

    unit_price = st.number_input("Unit Price ($)", min_value=0.0, key="price")

# ---------------- CALCULATIONS ----------------

revenue = order_quantity * unit_price
total_cost = order_quantity * unit_cost
actual_profit = revenue - total_cost

st.subheader("Quick Insights")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Revenue", f"${revenue:,.2f}")

with c2:
    st.metric("Cost", f"${total_cost:,.2f}")

with c3:
    st.metric("Profit", f"${actual_profit:,.2f}")

st.divider()

# ---------------- PREDICTION ----------------

if st.button("Predict Profit"):

    input_data = pd.DataFrame({
        'Customer_Age': [customer_age],
        'Customer_Gender': [customer_gender],
        'Country': [country],
        'Product_Category': [product_category],
        'Order_Quantity': [order_quantity],
        'Unit_Cost': [unit_cost],
        'Unit_Price': [unit_price]
    })

    if actual_profit <= 0:
        predicted_profit = actual_profit
        status = "loss"
    else:
        ml_prediction = float(model.predict(input_data)[0])
        predicted_profit = min(ml_prediction, actual_profit)
        status = "profit"

    st.subheader("Result")

    if status == "loss":
        st.error(f"Loss: ${abs(predicted_profit):,.2f}")
    else:
        st.success(f"Predicted Profit: ${predicted_profit:,.2f}")

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("Dashboard")

    st.write("Categories")
    st.write("Bikes, Accessories, Clothing")

    st.divider()

    st.write("Supported Countries")
    st.write("US, UK, Germany, France, Canada, Australia")

    st.divider()

    st.write("Current Time")
    st.write(datetime.now().strftime("%d %B %Y %I:%M:%S %p"))

# ---------------- FOOTER ----------------

st.divider()
st.caption("© 2026 AI Profit Prediction System")