import streamlit as st
import re

# --- CONFIGURASI HALAMAN & BACKGROUND ---
st.set_page_config(
    page_title="Stoikiometri Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# Menambahkan CSS Kustom untuk Background bertema Laboratorium / Kimia Digital
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    h1, h2, h3, .stMarkdown {
        color: #e0f7fa !important;
    }
    div[data-testid="stSidebar"] {
        background-color: #11222c !important;
    }
    .stButton>button {
        background-color: #00bcd4 !important;
        color: white !important;
        border-radius: 8px;
    }
    div[data-testid="stNotification"] {
        background-color: #1b3a4b !important;
        border-left: 5px solid #00bcd4 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE TABEL PERIODIK LENGKAP (Ar Semua Unsur) ---
# Berisi seluruh unsur dari Hidrogen (H) sampai Oganesson (Og)
AR_PERIODIK = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.63, 'As': 74.922, 'Se': 78.971, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.95, 'Tc': 98, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71,
    'Sb': 121.76, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91, 'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24, 'Pm': 145,
    'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93, 'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05, 'Lu': 174.97,
    'Hf': 178.49, 'Ta': 180.95, 'W': 183.84, 'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59, 'Tl': 204.38,
    'Pb': 207.2, 'Bi': 208.98, 'Po': 209, 'At': 210, 'Rn': 222, 'Fr': 223, 'Ra': 226, 'Ac': 227, 'Th': 232.04, 'Pa': 231.04, 'U': 238.03,
    'Np': 237, 'Pu': 244, 'Am': 243, 'Cm': 247, 'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257, 'Md': 258, 'No': 259, 'Lr': 262,
    'Rf': 267, 'Db': 268, 'Sg': 269, 'Bh': 270, 'Hs': 277, 'Mt': 278, 'Ds': 281, 'Rg': 282, 'Cn': 285, 'Nh': 286, 'Fl': 289, 'Mc': 290,
    'Lv': 293, 'Ts': 294, 'Og': 294
}

# Fungsi Pembantu Pengurai Rumus Kimia (Termasuk tanda kurung seperti Ca(OH)2)
def hitung_bm_dari_teks(rumus):
    def parse_formula(f):
        reg = r'([A-Z][a-z]*)(\d*)'
        res = re.findall(reg, f)
        return {element: int(count) if count else 1 for element, count in res}

    # Menangani tanda kurung di dalam rumus kimia
    while '(' in rumus:
        match = re.search(r'\(([^()]+)\)(\d*)', rumus)
        if match:
            sub_formula, sub_count = match.groups()
            sub_count = int(sub_count) if sub_count else 1
            sub_dict = parse_formula(sub_formula)
            expanded = "".join([f"{el}{num * sub_count}" for el, num in sub_dict.items()])
            rumus = rumus.replace(match.group(), expanded)
            
    komponen = parse_formula(rumus)
    total_bm = 0.0
    unsur_tidak_dikenal = []
    
    for unsur, jumlah in komponen.items():
        if unsur in AR_PERIODIK:
            total_bm += AR_PERIODIK[unsur] * jumlah
        else:
            unsur_tidak_dikenal.append(unsur)
            
    return total_bm, unsur_tidak_dikenal

# --- HALAMAN UTAMA: IDENTITAS KELOMPOK ---
st.title("🧮 Stoikiometri Kimia")
st.subheader("Oleh Kelompok 7 - Mata Kuliah Logika Pemrograman dan Komputer")

# Kotak Identitas Anggota
st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 25px;">
    <strong>Nama Anggota Kelompok:</strong><br>
    1. 2560556 - AFFAN IHSANUL FATAH<br>
    2. 2560618 - ELVIA ELVARITTA<br>
    3. 2560675 - MUHAMMAD AQIL<br>
    4. 2560739 - RAFI ALIFIA SHARIATI<br>
    5. 2560796 - TIARA APRILIANTI
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI ---
st.sidebar.image("https://img.icons8.com/fluent/96/000000/chemistry.png", width=80)
st.sidebar.header("Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Fitur Perhitungan:",
    ["Bobot Molekul (BM/Mr)", "Konversi Satuan Kimia", "Faktor Pengenceran"]
)

# ==========================================
# FEATURE 1: PERHITUNGAN BOBOT MOLEKUL TINGGAL KETIK
# ==========================================
if menu == "Bobot Molekul (BM/Mr)":
    st.header("🔬 Perhitungan Bobot Molekul Otomatis")
    st.write("Ketik rumus kimia senyawa langsung di bawah ini. Sistem mendukung penggunaan huruf kapital sensitif dan tanda kurung.")
    
    input_senyawa = st.text_input("Masukkan Rumus Kimia Senyawa (Contoh: H2SO4, NaOH, Ca(OH)2):", "H2SO4")
    
    if st.button("Hitung BM / Mr"):
        if input_senyawa:
            bm, error_unsur = hitung_bm_dari_teks(input_senyawa)
            if error_unsur:
                st.error(f"Unsur tidak dikenal atau salah ketik: {', '.join(error_unsur)}. Perhatikan huruf besar/kecilnya (Contoh: 'Na' bukan 'na').")
            elif bm == 0:
                st.warning("Format rumus tidak valid.")
            else:
                st.success(f"Bobot Molekul (BM) dari **{input_senyawa}** adalah: **{bm:.4f} g/mol**")
        else:
            st.warning("Silakan isi rumus kimia terlebih dahulu.")

# ==========================================
# FEATURE 2: KONVERSI SATUAN KIMIA MULTI-VARIABEL
# ==========================================
elif menu == "Konversi Satuan Kimia":
    st.header("🔄 Konversi Hubungan Satuan Kimia")
    st.write("Konversi terintegrasi antara Normalitas, Molaritas, Mol, Massa, dan Volume.")
    
    # Input data dasar yang dibutuhkan untuk kalkulasi silang
    col_a, col_b = st.columns(2)
    with col_a:
        mr_input = st.number_input("Massa Molar / Mr Senyawa (g/mol):", min_value=0.1, value=98.0, step=0.1)
    with col_b:
        valensi_input = st.number_input("Valensi / Ekivalen Zat (Untuk Normalitas):", min_value=1, value=2, step=1)

    st.markdown("---")
    
    opsi_asal = st.selectbox(
        "Pilih Satuan Yang Diketahui (Asal):",
        ["Massa (gram)", "Mol (n)", "Molaritas (M)", "Normalitas (N)"]
    )
    
    # Logika dinamis berdasarkan apa yang dipilih pengguna sebagai data asal
    if opsi_asal == "Massa (gram)":
        g = st.number_input("Masukkan Massa (gram):", min_value=0.0, value=9.8, step=0.1)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=100.0, step=10.0)
        
        if st.button("Konversi Satuan"):
            n = g / mr_input
            m = (g / mr_input) * (1000 / v_ml)
            norm = m * valensi_input
            
            st.success(f"**Hasil Konversi dari {g} gram zat dalam {v_ml} mL larutan:**")
            st.info(f"🔹 Jumlah Mol = **{n:.4f} mol**")
            st.info(f"🔹 Molaritas = **{m:.4f} M**")
            st.info(f"🔹 Normalitas = **{norm:.4f} N**")
            
    elif opsi_asal == "Mol (n)":
        n = st.number_input("Masukkan Jumlah Mol (mol):", min_value=0.0, value=0.1, step=0.01)
        v_ml = st.number_input("Masukkan Volume Larutan (mL) jika ingin mencari M & N:", min_value=0.1, value=100.0, step=10.0)
        
        if st.button("Konversi Satuan"):
            g = n * mr_input
            m = n * (1000 / v_ml)
            norm = m * valensi_input
            
            st.success(f"**Hasil Konversi dari {n} mol:**")
            st.info(f"🔹 Massa = **{g:.4f} gram**")
            st.info(f"🔹 Molaritas (dalam {v_ml} mL) = **{m:.4f} M**")
            st.info(f"🔹 Normalitas (dalam {v_ml} mL) = **{norm:.4f} N**")

    elif opsi_asal == "Molaritas (M)":
        m = st.number_input("Masukkan Molaritas (M):", min_value=0.0, value=1.0, step=0.1)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=250.0, step=10.0)
        
        if st.button("Konversi Satuan"):
            g = (m * mr_input * v_ml) / 1000
            n = (m * v_ml) / 1000
            norm = m * valensi_input
            
            st.success(f"**Hasil Konversi dari {m} M dalam {v_ml} mL:**")
            st.info(f"🔹 Massa Zat Terlarut = **{g:.4f} gram**")
            st.info(f"🔹 Jumlah Mol = **{n:.4f} mol**")
            st.info(f"🔹 Normalitas = **{norm:.4f} N**")

    elif opsi_asal == "Normalitas (N)":
        norm = st.number_input("Masukkan Normalitas (N):", min_value=0.0, value=1.0, step=0.1)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=250.0, step=10.0)
        
        if st.button("Konversi Satuan"):
            m = norm / valensi_input
            g = (m * mr_input * v_ml) / 1000
            n = (m * v_ml) / 1000
            
            st.success(f"**Hasil Konversi dari {norm} N dalam {v_ml} mL:**")
            st.info(f"🔹 Molaritas = **{m:.4f} M**")
            st.info(f"🔹 Massa Zat Terlarut = **{g:.4f} gram**")
            st.info(f"🔹 Jumlah Mol = **{n:.4f} mol**")

# ==========================================
# FEATURE 3: FAKTOR PENGENCERAN LENGKAP 4 VARIABEL
# ==========================================
elif menu == "Faktor Pengenceran":
    st.header("🧪 Perhitungan Faktor Pengenceran Lengkap")
    st.write("Gunakan rumus $V_1 \\times M_1 = V_2 \\times M_2$ untuk mencari nilai salah satu variabel.")
    
    target_cari = st.selectbox(
        "Pilih Variabel yang Ingin Dicari:",
        [
            "Konsentrasi Larutan Pekat (M1)", 
            "Volume Larutan Pekat (V1)", 
            "Konsentrasi Larutan Encer (M2)", 
            "Volume Larutan Encer (V2)"
        ]
    )
    
    st.markdown("---")
    
    if target_cari == "Konsentrasi Larutan Pekat (M1)":
        v1 = st.number_input("Volume Larutan Pekat yang diambil (V1 dalam mL):", min_value=0.01, value=10.0)
        m2 = st.number_input("Konsentrasi Larutan Encer Terbentuk (M2):", min_value=0.01, value=0.1)
        v2 = st.number_input("Volume Larutan Encer Terbentuk (V2 dalam mL):", min_value=0.01, value=100.0)
        
        if st.button("Hitung M1"):
            m1 = (m2 * v2) / v1
            st.success(f"Konsentrasi Larutan Pekat Asal (**M1**) adalah: **{m1:.4f} M (atau N)**")
            st.info(f"Faktor Pengenceran: **{v2/v1:.2f} kali**")
            
    elif target_cari == "Volume Larutan Pekat (V1)":
        m1 = st.number_input("Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=12.0)
        m2 = st.number_input("Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.5)
        v2 = st.number_input("Volume Larutan Encer yang Diinginkan (V2 dalam mL):", min_value=0.01, value=500.0)
        
        if st.button("Hitung V1"):
            if m1 >= m2:
                v1 = (m2 * v2) / m1
                st.success(f"Ambil **{v1:.4f} mL** larutan pekat, lalu encerkan sampai tanda batas volume **{v2} mL**.")
                st.info(f"Faktor Pengenceran: **{m1/m2:.2f} kali**")
            else:
                st.error("Error: Konsentrasi pekat (M1) harus lebih besar dari konsentrasi encer (M2)!")

    elif target_cari == "Konsentrasi Larutan Encer (M2)":
        m1 = st.number_input("Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=2.0)
        v1 = st.number_input("Volume Larutan Pekat yang diambil (V1 dalam mL):", min_value=0.01, value=25.0)
        v2 = st.number_input("Volume Larutan Setelah Diencerkan (V2 dalam mL):", min_value=0.01, value=250.0)
        
        if st.button("Hitung M2"):
            if v2 >= v1:
                m2 = (m1 * v1) / v2
                st.success(f"Konsentrasi Larutan Setelah Diencerkan (**M2**) adalah: **{m2:.4f} M (atau N)**")
                st.info(f"Faktor Pengenceran: **{v2/v1:.2f} kali**")
            else:
                st.error("Error: Volume akhir (V2) harus lebih besar dari volume awal (V1)!")

    elif target_cari == "Volume Larutan Encer (V2)":
        m1 = st.number_input("Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=6.0)
        v1 = st.number_input("Volume Larutan Pekat yang diambil (V1 dalam mL):", min_value=0.01, value=10.0)
        m2 = st.number_input("Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.1)
        
        if st.button("Hitung V2"):
            if m1 >= m2:
                v2 = (m1 * v1) / m2
                st.success(f"Volume akhir larutan encer (**V2**) adalah: **{v2:.2f} mL**")
                st.info(f"Artinya Anda perlu menambahkan aquades sebanyak **{v2 - v1:.2f} mL** ke dalam larutan pekat.")
            else:
                st.error("Error: Konsentrasi pekat (M1) harus lebih besar dari konsentrasi encer (M2)!")

# --- FOOTER ---
st.markdown("---")
st.caption("Aplikasi Logika Pemrograman & Komputer | Kelompok 7 | © 2026")
