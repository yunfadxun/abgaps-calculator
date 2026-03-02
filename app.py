import streamlit as st
import math

# Konfigurasi Halaman
st.set_page_config(page_title="Health Risk Calculator", page_icon="🏥")

# Judul dan Header
st.title("🏥 Kalkulator Risiko Kesehatan Kerja")
st.markdown("""
Aplikasi ini memprediksi probabilitas kejadian berdasarkan model regresi logistik. 
Silakan masukkan data pada kolom di bawah ini.
""")

# Sidebar untuk Input
st.sidebar.header("Input Variabel")

def user_input_features():
    usia = st.sidebar.selectbox("Rentang Usia:", (">=41", "<= 41"))
    dm = st.sidebar.selectbox("Riwayat Diabetes:", ("Tidak", "Ya"))
    htn = st.sidebar.selectbox("Status Hipertensi:", ("Normal", "Pre-HTN", "Stage 1 HTN", "Stage 2 HTN"))
    mk = st.sidebar.selectbox("Masa Kerja:", ("> 15 tahun", "5 - 15 tahun", "< 5 tahun"))
    dosis = st.sidebar.selectbox("Dosis Personal:", ("<=100", ">100"))
    apd = st.sidebar.selectbox("Penggunaan APD:", ("Selalu", "Kadang-kadang", "Tidak Menggunakan"))
    hobi = st.sidebar.selectbox("Hobi (Paparan Bising):", ("Tidak Ada", "Ada"))
    
    return {
        'usia': usia, 'dm': dm, 'htn': htn, 'mk': mk, 
        'dosis': dosis, 'apd': apd, 'hobi': hobi
    }

input_data = user_input_features()

# Logika Perhitungan (Fungsi Sigmoid)
def calculate_risk(data):
    z = -1.939
    if data['usia'] == ">=41": z += 2.076
    if data['dm'] == "Ya": z += 0.615
    
    if data['htn'] == "Pre-HTN": z += 0.157
    elif data['htn'] == "Stage 1 HTN": z += 0.736
    elif data['htn'] == "Stage 2 HTN": z += 0.884
    
    if data['mk'] == "5 - 15 tahun": z -= 1.774
    if data['dosis'] == ">100": z -= 0.396
    if data['apd'] == "Kadang-kadang": z += 0.220
    if data['hobi'] == "Ada": z -= 0.478
    
    prob = 1 / (1 + math.exp(-z))
    return prob * 100

probability = calculate_risk(input_data)

# Tampilan Hasil (Main Panel)
st.subheader("Hasil Analisis")
col1, col2 = st.columns(2)

with col1:
    if probability > 50:
        st.error(f"Probabilitas: {probability:.2f}%")
        st.warning("Kategori Risiko: TINGGI")
    elif probability > 20:
        st.warning(f"Probabilitas: {probability:.2f}%")
        st.info("Kategori Risiko: SEDANG")
    else:
        st.success(f"Probabilitas: {probability:.2f}%")
        st.write("Kategori Risiko: RENDAH")

with col2:
    st.write("**Ringkasan Input:**")
    st.write(f"- Usia: {input_data['usia']}")
    st.write(f"- Hipertensi: {input_data['htn']}")
    st.write(f"- APD: {input_data['apd']}")



st.markdown("---")
st.caption("Dikembangkan oleh Fadhaa Aditya Kautsar Murti, S.KM - Biostatistics Specialist")
