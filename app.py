import streamlit as st
import pandas as pd

# Database
data = [
    ["BCA", 1, 3.00], ["BCA", 3, 3.00], ["BCA", 6, 2.25], ["BCA", 12, 2.00],
    # Add other banks later if needed
]

df = pd.DataFrame(data, columns=["Bank", "Tenor", "Interest"])

# --- Page Setup ---
st.set_page_config(page_title="Simulasi Deposito", layout="centered")

# --- Header ---
st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/BCA_logo.svg", width=100)
st.title("Simulasi Deposito")
st.markdown("**Senantiasa di Sisi Anda**")

# --- Input: Nominal Penempatan ---
st.markdown("### Nominal Penempatan")
col1, col2 = st.columns([3, 1])
with col1:
    deposit = st.number_input("Masukkan jumlah penempatan:", min_value=8_000_000, step=1_000_000, format="%d")
with col2:
    st.write("")  # spacing

slider_val = st.slider("", 8_000_000, 100_000_000_000, deposit, step=1_000_000)
deposit = slider_val  # Sync with slider

# --- Input: Tenor ---
st.markdown("### Tenor")
tenor = st.slider("Tenor dalam bulan", 1, 12, 1)

# --- Interest Rate ---
bank = "BCA"
rate_row = df[(df["Bank"] == bank) & (df["Tenor"] == tenor)]
if not rate_row.empty:
    interest_rate = rate_row["Interest"].values[0]
else:
    interest_rate = 0.0

st.markdown(f"### Suku Bunga\n{interest_rate:.2f} %")

# --- Calculate Interest ---
def calculate_return(nominal, rate, tenor_months):
    interest = nominal * (rate / 100) * (tenor_months * 30 / 365)
    net_interest = interest * 0.8  # 20% tax
    return nominal + net_interest, net_interest

total, net_earning = calculate_return(deposit, interest_rate, tenor)

# --- Button ---
if st.button("Hitung Simulasi"):
    st.markdown("### 💡 Hasil Simulasi")
    st.write(f"**Bunga Setelah Pajak (20%)**: Rp {net_earning:,.0f}")
    st.write(f"**Total Pencairan**: Rp {total:,.0f}")

# --- Footnote ---
st.markdown("---")
st.caption("Catatan: Perhitungan ini hanya sebagai alat bantu simulasi investasi dan tidak dimaksudkan untuk menyediakan rekomendasi apa pun.")
st.caption("Asumsi: 1 bulan = 30 hari, dan 1 tahun = 365 hari")