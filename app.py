import streamlit as st
import pandas as pd

# --- Data suku bunga BCA ---
data = [
    ["BCA", 1, 3.00], ["BCA", 3, 3.00], ["BCA", 6, 2.25], ["BCA", 12, 2.00],
]
df = pd.DataFrame(data, columns=["Bank", "Tenor", "Interest"])

# --- Setup UI ---
st.set_page_config(page_title="Simulasi Deposito", layout="centered")
st.title("Simulasi Deposito")
st.markdown("**Senantiasa di Sisi Anda**")

# --- Input Nominal Penempatan ---
st.markdown("### Nominal Penempatan")
deposit = st.number_input(
    "Masukkan jumlah penempatan:", min_value=8_000_000, step=1_000_000
)
st.caption(f"Format: Rp {deposit:,.0f}")

# --- Input Tenor: pilihan yang tersedia di data ---
st.markdown("### Tenor")
available_tenors = df["Tenor"].unique().tolist()
tenor = st.select_slider("Pilih tenor yang tersedia", options=available_tenors, value=1)

# --- Cari suku bunga ---
rate_row = df[(df["Bank"] == "BCA") & (df["Tenor"] == tenor)]
interest_rate = rate_row["Interest"].values[0] if not rate_row.empty else 0.0
st.markdown(f"### Suku Bunga\n{interest_rate:.2f} %")

# --- Fungsi hitung hasil deposito ---
def calculate_return(nominal, rate, tenor_months):
    interest = nominal * (rate / 100) * (tenor_months * 30 / 365)
    net_interest = interest * 0.8  # 20% pajak
    return nominal + net_interest, net_interest

# --- Tombol hitung ---
if st.button("Hitung Simulasi"):
    total, net_earning = calculate_return(deposit, interest_rate, tenor)
    st.markdown("### 💡 Hasil Simulasi")
    st.write(f"**Bunga Setelah Pajak (20%)**: Rp {net_earning:,.0f}")
    st.write(f"**Total Pencairan**: Rp {total:,.0f}")

# --- Catatan bawah ---
st.markdown("---")
st.caption("Catatan: Perhitungan ini hanya sebagai alat bantu simulasi investasi dan tidak dimaksudkan untuk menyediakan rekomendasi apa pun.")
st.caption("Asumsi: 1 bulan = 30 hari, dan 1 tahun = 365 hari")