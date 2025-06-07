import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Interest rate database
# ------------------------------
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

# ------------------------------
# UI - Sidebar Inputs
# ------------------------------
st.title("Simulasi Deposito Multi-Bank")

st.subheader("💰 Nominal Penempatan")
deposit = st.slider("Masukkan nominal penempatan", 8_000_000, 100_000_000_000, 8_000_000, step=1_000_000)

st.subheader("⏱️ Pilih Tenor (bulan)")
tenor = st.slider("Tenor dalam bulan", 1, 12, 1)

st.subheader("🏦 Pilih 2 Bank untuk dibandingkan")
banks = df["Bank"].unique()
bank_1 = st.selectbox("Bank 1", banks, index=0)
bank_2 = st.selectbox("Bank 2", banks, index=1)

# ------------------------------
# Calculation function
# ------------------------------
def calculate_return(nominal, rate, tenor_months):
    interest = nominal * (rate / 100) * (tenor_months * 30 / 365)
    net_interest = interest * 0.8  # 20% tax
    return nominal + net_interest

# ------------------------------
# Get interest rates from database
# ------------------------------
def get_rate(bank, tenor):
    result = df[(df["Bank"] == bank) & (df["Tenor"] == tenor)]
    return result["Interest"].values[0] if not result.empty else 0.0

rate1 = get_rate(bank_1, tenor)
rate2 = get_rate(bank_2, tenor)

# Calculate returns
return1 = calculate_return(deposit, rate1, tenor)
return2 = calculate_return(deposit, rate2, tenor)
savings_return = deposit  # base case: savings (assume no interest)

# ------------------------------
# Display Results
# ------------------------------
st.markdown("### 💹 Hasil Simulasi:")
st.write(f"**{bank_1}** (Bunga {rate1:.2f}%) → Rp {return1:,.0f}")
st.write(f"**{bank_2}** (Bunga {rate2:.2f}%) → Rp {return2:,.0f}")
st.write(f"**Rekening Tabungan** (0%) → Rp {savings_return:,.0f}")

# ------------------------------
# Line Chart - growth over time
# ------------------------------
months = list(range(1, tenor + 1))
growth1 = [calculate_return(deposit, rate1, m) for m in months]
growth2 = [calculate_return(deposit, rate2, m) for m in months]
savings = [deposit for _ in months]

chart_data = pd.DataFrame({
    "Rekening Tabungan": savings,
    f"{bank_1}": growth1,
    f"{bank_2}": growth2
}, index=[f"{m} bln" for m in months])

st.line_chart(chart_data)