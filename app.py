import streamlit as st
import pandas as pd

st.write("Hi Lia")

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

st.set_page_config(page_title="Time Deposit", layout="wide")
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
Time Deposit
</h1>
""", unsafe_allow_html=True)

st.markdown("**Tired of visiting multiple websites to compare time deposit returns? This platform helps you simulate and compare time deposit returns from various banks—including the latest digital banks tailored for Gen Z. Now, you can find the best rates all in one place—fast, simple, and hassle-free.**")

# --- CSS: Perbesar Slider dan Handle (5x Ukuran Normal) ---
st.markdown("""
    <style>
    .stSlider > div[data-baseweb="slider"] > div {
        height: 60px;
    }
    .stSlider .css-1c5b0k4 {
        height: 60px !important;
        width: 60px !important;
        border-radius: 30px;
        background-color: #2c8cff;
    }
    .stSlider label {
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Pilih Bank ---
selected_bank = st.selectbox("Pilih Bank", sorted(df["Bank"].unique()))
filtered_df = df[df["Bank"] == selected_bank]

# --- Input Penempatan Dana ---
st.markdown("### Nominal Penempatan")
deposit = st.number_input(
    "Masukkan jumlah penempatan:", min_value=8_000_000, step=1_000_000
)
st.caption(f"Format: Rp {deposit:,.0f}")

# --- Tenor Slider (otomatis dari bank terpilih) ---
st.markdown("### Tenor")
available_tenors = sorted(filtered_df["Tenor"].unique())
tenor = st.select_slider("Pilih tenor yang tersedia", options=available_tenors, value=available_tenors[0])

# --- Ambil Suku Bunga ---
rate_row = filtered_df[filtered_df["Tenor"] == tenor]
interest_rate = rate_row["Interest"].values[0] if not rate_row.empty else 0.0
st.markdown(f"### Suku Bunga\n{interest_rate:.2f} %")

# --- Fungsi Simulasi Perhitungan Bunga ---
def calculate_return(nominal, rate, tenor_months):
    interest = nominal * (rate / 100) * (tenor_months * 30 / 365)
    net_interest = interest * 0.8  # dikurangi pajak 20%
    return nominal + net_interest, net_interest

# --- Tombol Hitung ---
if st.button("Hitung Simulasi"):
    total, net_earning = calculate_return(deposit, interest_rate, tenor)
    st.markdown("### 💡 Hasil Simulasi")
    st.write(f"**Bunga Setelah Pajak (20%)**: Rp {net_earning:,.0f}")
    st.write(f"**Total Pencairan**: Rp {total:,.0f}")

# --- Footer ---
st.markdown("---")
st.caption("Catatan: Perhitungan ini hanya sebagai alat bantu simulasi dan tidak dimaksudkan untuk menyediakan rekomendasi apa pun.")
st.caption("Asumsi: 1 bulan = 30 hari, dan 1 tahun = 365 hari.")