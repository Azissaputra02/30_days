import streamlit as st
import pandas as pd

# --- Data suku bunga BCA ---
data = [
    ["BCA", 1, 3.00], ["BCA", 3, 3.00], ["BCA", 6, 2.25], ["BCA", 12, 2.00],
]
df = pd.DataFrame(data, columns=["Bank", "Tenor", "Interest"])

# --- Setup UI ---
st.set_page_config(page_title="Simulasi Deposito", layout="centered")
st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/BCA_logo.svg", width=100)
st.title("Simulasi Deposito")
st.markdown("**Senantiasa di Sisi Anda**")

# --- Nominal Penempatan (terhubung antara input manual dan slider) ---
st.markdown("### Nominal Penempatan")
min_val, max_val = 8_000_000, 100_000_000_000

# State sync
if "deposit" not in st.session_state:
    st.session_state.deposit = 8_000_000

col1, col2 = st.columns([3, 1])
with col1:
    deposit_input = st.number_input("Masukkan jumlah penempatan:", min_value=min_val, max_value=max_val, step=1_000_000, format="%,d", key="deposit")
with col2:
    st.write("")  # spacer

deposit_slider = st.slider("Geser untuk ubah nominal", min_val, max_val, st.session_state.deposit, step=1_000_000, format="%,d")

# Sinkronisasi dua arah
if deposit_input != deposit_slider:
    st.session_state.deposit = deposit_slider

# --- Tenor: hanya pilihan yang tersedia ---
st.markdown("### Tenor")
available_tenors = df["Tenor"].unique().tolist()
tenor = st.select_slider("Pilih tenor yang tersedia", options=available_tenors, value=1)

# --- Ambil suku bunga dari database ---
rate_row = df[(df["Bank"] == "BCA") & (df["Tenor"] == tenor)]
interest_rate = rate_row["Interest"].values[0] if not rate_row.empty else 0.0

st.markdown(f"### Suku Bunga\n{interest_rate:.2f} %")

# --- Fungsi hitung bunga deposito setelah pajak ---
def calculate_return(nominal, rate, tenor_months):
    interest = nominal * (rate / 100) * (tenor_months * 30 / 365)
    net_interest = interest * 0.8  # 20% pajak
    return nominal + net_interest, net_interest

# --- Tombol Hitung ---
if st.button("Hitung Simulasi"):
    total, net_earning = calculate_return(st.session_state.deposit, interest_rate, tenor)
    st.markdown("### 💡 Hasil Simulasi")
    st.write(f"**Bunga Setelah Pajak (20%)**: Rp {net_earning:,.0f}")
    st.write(f"**Total Pencairan**: Rp {total:,.0f}")

# --- Catatan bawah ---
st.markdown("---")
st.caption("Catatan: Perhitungan ini hanya sebagai alat bantu simulasi investasi dan tidak dimaksudkan untuk menyediakan rekomendasi apa pun.")
st.caption("Asumsi: 1 bulan = 30 hari, dan 1 tahun = 365 hari")