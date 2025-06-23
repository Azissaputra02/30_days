import streamlit as st
import pandas as pd

# --- Data Suku Bunga dari Semua Bank ---
data = [
    ["BCA", 1, 3.00], ["BCA", 3, 3.00], ["BCA", 6, 2.25], ["BCA", 12, 2.00],
    ["BNI", 1, 2.25], ["BNI", 3, 2.50], ["BNI", 6, 2.75], ["BNI", 12, 3.00],
    ["BRI", 1, 3.35], ["BRI", 3, 3.50], ["BRI", 6, 3.00], ["BRI", 12, 3.00],
    ["CIMB", 1, 2.75], ["CIMB", 3, 3.35], ["CIMB", 6, 3.35], ["CIMB", 12, 3.35],
    ["Danamon", 1, 3.25], ["Danamon", 3, 3.50], ["Danamon", 6, 4.00], ["Danamon", 9, 4.00], ["Danamon", 12, 4.25],
    ["Mandiri", 1, 2.25], ["Mandiri", 3, 2.25], ["Mandiri", 6, 2.50], ["Mandiri", 12, 2.50],
    ["Allo Bank", 1, 5.00], ["Allo Bank", 3, 6.50], ["Allo Bank", 6, 7.00], ["Allo Bank", 12, 7.50],
    ["Bank Jago", 1, 5.00], ["Bank Jago", 3, 5.50], ["Bank Jago", 6, 5.50], ["Bank Jago", 12, 5.50],
    ["Bank Neo", 1, 6.25], ["Bank Neo", 2, 6.75], ["Bank Neo", 6, 7.25], ["Bank Neo", 12, 8.00],
    ["Seabank", 1, 4.50], ["Seabank", 3, 5.25], ["Seabank", 6, 5.75], ["Seabank", 12, 6.00],
    ["Superbank", 1, 7.50], ["Superbank", 3, 7.50], ["Superbank", 6, 7.50], ["Superbank", 9, 7.50], ["Superbank", 12, 7.50],
]
df = pd.DataFrame(data, columns=["Bank", "Tenor", "Interest"])

# --- Set Page Config ---
st.set_page_config(page_title="Time Deposit Comparison", layout="wide")

# --- Apply White Background CSS ---
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
<h1 style="
    font-size: 3em;
    font-weight: 900;
    background: linear-gradient(to right, #8e44ad, #2980b9, #e84393);
    -webkit-background-clip: text;
    color: transparent;
    text-align: left;
    margin-top: -20px;
">
Time Deposit Comparison
</h1>
""", unsafe_allow_html=True)

st.markdown("Compare time deposit returns from two banks and find which gives you a better deal—all in one place.")

# --- Select Banks ---
col1, col2 = st.columns(2)
with col1:
    bank1 = st.selectbox("Choose First Bank", sorted(df["Bank"].unique()), key="bank1")
with col2:
    bank2 = st.selectbox("Choose Second Bank", sorted(df["Bank"].unique()), key="bank2")

# --- Input Deposit Amount ---
deposit = st.number_input("Input your deposit amount (Rp):", min_value=8_000_000, step=1_000_000, format="%i")
st.caption(f"Formatted: Rp {deposit:,.0f}")

# --- Common Tenor Options ---
common_tenors = sorted(set(df[df["Bank"] == bank1]["Tenor"]).intersection(df[df["Bank"] == bank2]["Tenor"]))
tenor = st.select_slider("Tenor (Month)", options=common_tenors, value=common_tenors[0])

# --- Get Interest Rates ---
rate1 = df[(df["Bank"] == bank1) & (df["Tenor"] == tenor)]["Interest"].values[0]
rate2 = df[(df["Bank"] == bank2) & (df["Tenor"] == tenor)]["Interest"].values[0]

# --- Calculate Returns ---
def calculate_return(nominal, rate, tenor_months):
    days = 365 if tenor_months == 12 else tenor_months * 30
    gross_interest = nominal * (rate / 100) * (days / 365)
    net_interest = gross_interest * 0.8
    total = nominal + net_interest
    return total, net_interest

# --- Compare Button ---
if st.button("Compare"):
    total1, net1 = calculate_return(deposit, rate1, tenor)
    total2, net2 = calculate_return(deposit, rate2, tenor)

    result = pd.DataFrame({
        "Description": ["Initial Deposit", "Net Interest (after 20% tax)", "Total Received"],
        bank1: [deposit, net1, total1],
        bank2: [deposit, net2, total2],
        "Difference": ["-", f"Rp {net2 - net1:,.0f}", f"Rp {total2 - total1:,.0f}"]
    })

    st.markdown("### Comparison Result")
    st.table(result.style.format({bank1: "Rp {:,.0f}", bank2: "Rp {:,.0f}"}))

    st.warning("""
💡 **Note**: Make sure you're comparing banks that you already use.  
- Transferring funds to unfamiliar or digital-only banks may incur fees.  
- Higher interest rates (e.g., >4.25%) may reflect higher risk or limited LPS protection.
""")

# --- Footer ---
st.markdown("---")
st.caption("Simulation only. Assumes 1 month = 30 days and 1 year = 365 days.")