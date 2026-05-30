import streamlit as st
import re
import base64

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Stoikiometri Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# Fungsi untuk mengonversi gambar lokal menjadi format base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tentukan jalur file gambar latar belakang (pastikan file ini ada di folder yang sama)
background_image_file = "image_6.png"

try:
    # Mengonversi gambar menjadi base64
    bin_str = get_base64_of_bin_file(background_image_file)
    
    # --- PERBAIKAN 4: LATAR BELAKANG GRADIEN & ELEMEN KIMIA ---
    st.markdown(f"""
        <style>
        /* Gradien latar belakang cerah (biru muda ke teal muda) */
        .stApp {{
            background-color: #f0fdfd;
            background-image: 
                /* Latar belakang grafis kimia dari gambar 6 */
                linear-gradient(to bottom right, rgba(235, 253, 253, 0.9), rgba(204, 251, 241, 0.9)),
                url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #1e293b;
        }}
        
        /* Navigasi Sidebar */
        div[data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-right: 2px solid #e2e8f0;
        }}
        
        /* Header & Teks */
        h1, h2, h3 {{
            color: #0f766e !important;
            font-weight: 700;
        }}
        
        /* Kotak Identitas Kelompok */
        .identitas-box {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #0d9488;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
        }}
        
        /* Tombol Utama */
        .stButton>button {{
            background-color: #0d9488 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            border: none !important;
            width: 100%;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #0f766e !important;
            transform: translateY(-1px);
        }}
        
        /* Kotak Input */
        div[data-testid="stNumberInput"] label {{
            color: #0f766e !important;
            font-weight: 600;
        }}

        /* Kotak Hasil (Alert) Kontras Tinggi */
        div[data-testid="stNotification"] {{
            background-color: rgba(240, 253, 250, 0.9) !important;
            border: 1px solid #99f6e4 !important;
            border-left: 6px solid #0d9488 !important;
            color: #115e59 !important;
        }}
        div[data-testid="stNotification"] p {{
            color: #115e59 !important;
            font-weight: 600;
        }}
        </style>
        """, unsafe_allow_html=True)

except FileNotFoundError:
    # Fallback jika gambar tidak ditemukan
    st.warning(f"Gambar latar belakang '{background_image_file}' tidak ditemukan. Menggunakan fallback gradien saja.")
    st.markdown("""
        <style>
        .stApp {{
            background-color: #f0fdfd;
            background-image: 
                linear-gradient(to bottom right, rgba(235, 253, 253, 0.95), rgba(204, 251, 241, 0.95));
            color: #1e293b;
        }}
        /* Sisanya sama */
        div[data-testid="stSidebar"] {{ background-color: rgba(255, 255, 255, 0.95) !important; }}
        h1, h2, h3 {{ color: #0f766e !important; }}
        /* ... */
        </style>
        """, unsafe_allow_html=True)

# --- DATABASE TABEL PERIODIK LENGKAP ---
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

# --- FUNGSI FORMATTING HASIL ---
def format_hasil(nilai):
    # Mengonversi titik menjadi koma
    return f"{nilai:.4f}".replace('.', ',')

def format_mol(nilai):
    # Mengonversi titik menjadi koma
    return f"{nilai:.4f}".replace('.', ',')

def format_volume(nilai):
    # Mengonversi titik menjadi koma
    return f"{nilai:.1f}".replace('.', ',')

def hitung_bm_dari_teks(rumus):
    def parse_formula(f):
        reg = r'([A-Z][a-z]*)(\d*)'
        res = re.findall(reg, f)
        return {element: int(count) if count else 1 for element, count in res}

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

# --- JUDUL & IDENTITAS KELOMPOK ---
st.title("🧪 Stoikiometri Kimia")
st.subheader("Mata Kuliah Logika Pemrograman dan Komputer")

st.markdown("""
<div class="identitas-box">
    <span style="color: #0f766e; font-weight: bold; font-size: 1.1rem;">Kelompok 7:</span><br>
    <table style="width:100%; border:none; margin-top:8px; color:#334155;">
        <tr><td>1. 2560556 - AFFAN IHSANUL FATAH</td></tr>
        <tr><td>2. 2560618 - ELVIA ELVARITTA</td></tr>
        <tr><td>3. 2560675 - MUHAMMAD AQIL</td></tr>
        <tr><td>4. 2560739 - RAFI ALIFIA SHARIATI</td></tr>
        <tr><td>5. 2560796 - TIARA APRILIANTI</td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI ---
st.sidebar.header("🧭 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Fitur Perhitungan:",
    ["Bobot Molekul (BM/Mr)", "Konversi Satuan Kimia", "Faktor Pengenceran"]
)

# ==========================================
# FEATURE 1: BOBOT MOLEKUL (BM/Mr)
# ==========================================
if menu == "Bobot Molekul (BM/Mr)":
    st.header("🔬 Perhitungan Bobot Molekul Otomatis")
    st.write("Ketik rumus molekul senyawa kimia secara langsung untuk mengetahui berat molekulnya.")
    
    input_senyawa = st.text_input("Masukkan Rumus Kimia Senyawa (Contoh: H2SO4, Ca(OH)2, NaCl):", "H2SO4")
    
    if st.button("Hitung BM / Mr"):
        if input_senyawa:
            bm, error_unsur = hitung_bm_dari_teks(input_senyawa)
            if error_unsur:
                st.error(f"Unsur tidak dikenal: {', '.join(error_unsur)}. Gunakan huruf besar di awal unsur (Contoh: 'NaOH' bukan 'naoh').")
            elif bm == 0:
                st.warning("Format rumus tidak valid.")
            else:
                st.success(f"Bobot Molekul (BM) dari {input_senyawa} adalah: {format_hasil(bm)} g/mol")
        else:
            st.warning("Silakan isi rumus kimia terlebih dahulu.")

# ==========================================
# FEATURE 2: REVISI KONVERSI SATUAN (DARI -> KE)
# ==========================================
elif menu == "Konversi Satuan Kimia":
    st.header("🔄 Konversi Hubungan Satuan Kimia")
    st.write("Silakan tentukan satuan awal dan satuan tujuan konversi yang Anda inginkan.")
    
    # Input parameter dasar senyawa
    c1, c2 = st.columns(2)
    with c1:
        mr_val = st.number_input("Massa Molar / Mr Senyawa (g/mol):", min_value=0.1, value=98.0, step=0.1)
    with c2:
        val_val = st.number_input("Valensi / Ekivalen Zat (Untuk Normalitas):", min_value=1, value=2, step=1)
        
    st.markdown("### ⚙️ Pengaturan Alur Konversi")
    
    col_from, col_to = st.columns(2)
    with col_from:
        satuan_asal = st.selectbox(
            "Pilih Satuan Asal (Yang Diketahui):",
            ["Massa (gram)", "Mol (mol)", "Molaritas (M)", "Normalitas (N)"]
        )
    with col_to:
        daftar_tujuan = ["Massa (gram)", "Mol (mol)", "Molaritas (M)", "Normalitas (N)"]
        if satuan_asal in daftar_tujuan:
            daftar_tujuan.remove(satuan_asal)
        satuan_tujuan = st.selectbox("Pilih Satuan Tujuan (Yang Dicari):", daftar_tujuan)

    st.markdown("---")
    
    # --- PERBAIKAN 2: LOGIKA KONVERSI MASSA KE MOL ---
    if satuan_asal == "Massa (gram)":
        g = st.number_input("Masukkan Nilai Massa (gram):", min_value=0.0, value=9.8)
        
        # Logika dinamis untuk volume
        if satuan_tujuan in ["Molaritas (M)", "Normalitas (N)"]:
            v_ml = st.number_input("Masukkan Volume Larutan (mL) [Dibutuhkan untuk M dan N]:", min_value=0.1, value=100.0)
        
        if st.button("Proses Konversi"):
            mol = g / mr_val # Koreksi: Hitung mol dulu
            molaritas = mol * (1000 / v_ml) if 'v_ml' in locals() else 0
            normalitas = molaritas * val_val if 'v_ml' in locals() else 0
            
            if satuan_tujuan == "Mol (mol)":
                st.success(f"Hasil: {format_hasil(g)} gram = {format_mol(mol)} mol")
            elif satuan_tujuan == "Molaritas (M)":
                st.success(f"Hasil: {format_hasil(g)} gram dalam {format_volume(v_ml)} mL = {format_hasil(molaritas)} M")
            elif satuan_tujuan == "Normalitas (N)":
                st.success(f"Hasil: {format_hasil(g)} gram dalam {format_volume(v_ml)} mL = {format_hasil(normalitas)} N")

    elif satuan_asal == "Mol (mol)":
        mol = st.number_input("Masukkan Nilai Jumlah Mol (mol):", min_value=0.0, value=0.1)
        
        # Logika dinamis untuk volume
        if satuan_tujuan in ["Molaritas (M)", "Normalitas (N)"]:
            v_ml = st.number_input("Masukkan Volume Larutan (mL) [Dibutuhkan untuk M dan N]:", min_value=0.1, value=100.0)
        
        if st.button("Proses Konversi"):
            g = mol * mr_val
            molaritas = mol * (1000 / v_ml) if 'v_ml' in locals() else 0
            normalitas = molaritas * val_val if 'v_ml' in locals() else 0
            
            if satuan_tujuan == "Massa (gram)":
                st.success(f"Hasil: {format_mol(mol)} mol = {format_hasil(g)} gram")
            elif satuan_tujuan == "Molaritas (M)":
                st.success(f"Hasil: {format_mol(mol)} mol dalam {format_volume(v_ml)} mL = {format_hasil(molaritas)} M")
            elif satuan_tujuan == "Normalitas (N)":
                st.success(f"Hasil: {format_mol(mol)} mol dalam {format_volume(v_ml)} mL = {format_hasil(normalitas)} N")

    elif satuan_asal == "Molaritas (M)":
        molaritas = st.number_input("Masukkan Nilai Molaritas (M):", min_value=0.0, value=1.0)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=250.0)
        
        if st.button("Proses Konversi"):
            g = (molaritas * mr_val * v_ml) / 1000
            mol = (molaritas * v_ml) / 1000
            normalitas = molaritas * val_val
            
            if satuan_tujuan == "Massa (gram)":
                st.success(f"Hasil: {format_hasil(molaritas)} M dalam {format_volume(v_ml)} mL = {format_hasil(g)} gram")
            elif satuan_tujuan == "Mol (mol)":
                st.success(f"Hasil: {format_hasil(molaritas)} M dalam {format_volume(v_ml)} mL = {format_mol(mol)} mol")
            elif satuan_tujuan == "Normalitas (N)":
                st.success(f"Hasil: {format_hasil(molaritas)} M = {format_hasil(normalitas)} N")

    elif satuan_asal == "Normalitas (N)":
        normalitas = st.number_input("Masukkan Nilai Normalitas (N):", min_value=0.0, value=1.0)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=250.0)
        
        if st.button("Proses Konversi"):
            molaritas = normalitas / val_val
            g = (molaritas * mr_val * v_ml) / 1000
            mol = (molaritas * v_ml) / 1000
            
            if satuan_tujuan == "Molaritas (M)":
                st.success(f"Hasil: {format_hasil(normalitas)} N = {format_hasil(molaritas)} M")
            elif satuan_tujuan == "Massa (gram)":
                st.success(f"Hasil: {format_hasil(normalitas)} N dalam {format_volume(v_ml)} mL = {format_hasil(g)} gram")
            elif satuan_tujuan == "Mol (mol)":
                st.success(f"Hasil: {format_hasil(normalitas)} N dalam {format_volume(v_ml)} mL = {format_mol(mol)} mol")

# ==========================================
# FEATURE 3: FAKTOR PENGENCERAN
# ==========================================
elif menu == "Faktor Pengenceran":
    st.header("🧪 Perhitungan Faktor Pengenceran")
    st.write("Gunakan rumus pengenceran murni $V_1 \\times M_1 = V_2 \\times M_2$")
    
    target_cari = st.selectbox(
        "Pilih Variabel yang Ingin Anda Cari:",
        [
            "Konsentrasi Larutan Pekat (M1)", 
            "Volume Larutan Pekat (V1)", 
            "Konsentrasi Larutan Encer (M2)", 
            "Volume Larutan Encer (V2)"
        ]
    )
    
    st.markdown("### 📝 Kotak Input Parameter")
    
    # Modifikasi pelabelan form input agar eksplisit dan mudah dibaca user
    if target_cari == "Konsentrasi Larutan Pekat (M1)":
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=10.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer Terbentuk (M2):", min_value=0.01, value=0.1)
        v2 = st.number_input("Masukkan Volume Larutan Encer Terbentuk (V2) dalam mL:", min_value=0.01, value=100.0)
        
        if st.button("Hitung M1"):
            m1 = (m2 * v2) / v1
            st.success(f"Hasil Perhitungan: Konsentrasi Larutan Pekat Asal (M1) = {format_hasil(m1)} M (atau N)")
            # --- PERBAIKAN 1: HAPUS TULISAN FAKTOR PENGENCERAN ---
            # st.info(f"Faktor Pengenceran yang dilakukan: {format_hasil(v2/v1)} kali")
            
    elif target_cari == "Volume Larutan Pekat (V1)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=12.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.5)
        v2 = st.number_input("Masukkan Volume Larutan Encer yang Diinginkan (V2) dalam mL:", min_value=0.01, value=500.0)
        
        if st.button("Hitung V1"):
            if m1 >= m2:
                v1 = (m2 * v2) / m1
                st.success(f"Hasil Perhitungan: Ambil {format_hasil(v1)} mL larutan pekat (V1), lalu encerkan hingga {format_volume(v2)} mL.")
                # st.info(f"Faktor Pengenceran: {format_hasil(m1/m2)} kali")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari konsentrasi encer (M2)!")

    elif target_cari == "Konsentrasi Larutan Encer (M2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=2.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=25.0)
        v2 = st.number_input("Masukkan Volume Larutan Setelah Diencerkan (V2) dalam mL:", min_value=0.01, value=250.0)
        
        if st.button("Hitung M2"):
            if v2 >= v1:
                m2 = (m1 * v1) / v2
                st.success(f"Hasil Perhitungan: Konsentrasi Larutan Setelah Diencerkan (M2) = {format_hasil(m2)} M (atau N)")
                # st.info(f"Faktor Pengenceran: {format_hasil(v2/v1)} kali")
            else:
                st.error("Gagal: Volume akhir (V2) harus lebih besar daripada volume awal (V1)!")

    elif target_cari == "Volume Larutan Encer (V2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=6.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=10.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.1)
        
        if st.button("Hitung V2"):
            if m1 >= m2:
                v2 = (m1 * v1) / m2
                st.success(f"Hasil Perhitungan: Volume Akhir Larutan Encer (V2) = {format_volume(v2)} mL")
                st.info(f"Tambahkan air aquades sebanyak {format_volume(v2 - v1)} mL ke dalam labu takar.")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari konsentrasi encer (M2)!")

# --- FOOTER ---
st.markdown("---")
st.caption("Aplikasi Logika Pemrograman & Komputer | Kelompok 7 | © 2026")
