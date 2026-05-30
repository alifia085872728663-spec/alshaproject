import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Stoikiometri Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# --- REVISI TOTAL: GRADASI & ELEMEN KIMIA MURNI CSS/SVG (TANPA CEK FILE GAMBAR) ---
st.markdown("""
    <style>
    /* Background dengan gradasi warna Lembut: Biru -> Putih -> Kuning */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #ffffff 50%, #fef9c3 100%) !important;
        background-attachment: fixed !important;
        color: #1e293b;
    }

    /* Elemen Grafis Kimia Transparan (Erlenmeyer, Labu, Atom, Molekul) Langsung via SVG */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.08; /* Transparansi elemen kimia agar tidak menutupi teks */
        z-index: 0;
        background-image: 
            /* Gelas Kimia & Ikatan Molekul di Kiri Bawah */
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%230284c7' stroke-width='3'%3E%3Cpath d='M80 650 L140 650 L120 530 L100 530 Z' /%3E%3Cpath d='M100 560 L140 560 M105 590 L135 590 M110 620 L130 620' /%3E%3Ccircle cx='190' cy='520' r='12' /%3E%3Ccircle cx='250' cy='490' r='18' /%3E%3Ccircle cx='290' cy='540' r='10' /%3E%3Cline x1='190' y1='520' x2='235' y2='495' /%3E%3Cline x1='250' y1='490' x2='290' y2='530' /%3E%3C/g%3E%3C/svg%3E"),
            /* Erlenmeyer & Struktur Cincin Benzena di Kanan Atas */
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%230369a1' stroke-width='2.5'%3E%3Cpath d='M680 150 L680 190 L630 300 L730 300 L680 190' /%3E%3Cpath d='M645 270 L715 270 M655 240 L705 240' /%3E%3Cpolygon points='600,100 640,80 680,100 680,140 640,160 600,140' /%3E%3Cpolygon points='560,140 600,160 600,200 560,220 520,200 520,140' /%3E%3C/g%3E%3C/svg%3E");
        background-position: left bottom, right top;
        background-repeat: no-repeat;
        background-size: 380px, 380px;
    }
    
    /* Memastikan konten utama berada di atas background */
    .main .block-container {
        position: relative;
        z-index: 1;
    }
    
    /* Navigasi Sidebar */
    div[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Judul & Sub-judul */
    h1, h2, h3 {
        color: #0369a1 !important;
        font-weight: 700;
    }
    
    /* Kotak Kelompok */
    .identitas-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #0ea5e9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* Tombol Utama */
    .stButton>button {
        background-color: #0ea5e9 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        padding: 10px 0px;
    }
    .stButton>button:hover {
        background-color: #0284c7 !important;
    }
    
    /* Kotak Hasil Output (Alert) */
    div[data-testid="stNotification"] {
        background-color: rgba(240, 253, 250, 0.95) !important;
        border: 1px solid #99f6e4 !important;
        border-left: 6px solid #0d9488 !important;
    }
    div[data-testid="stNotification"] p {
        color: #115e59 !important;
        font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE TABEL PERIODIK ---
AR_PERIODIK = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38, 'Ag': 107.87, 'I': 126.90, 'Ba': 137.33, 'Pb': 207.2
}

# --- FUNGSI FORMATTING INDONESIA (MENGUBAH TITIK MENJADI KOMA) ---
def format_koma(nilai):
    return f"{nilai:.4f}".rstrip('0').rstrip('.').replace('.', ',')

def format_koma_v(nilai):
    return f"{nilai:.2f}".replace('.', ',')

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

# --- IDENTITAS KELOMPOK ---
st.title("🧪 Aplikasi Stoikiometri Kimia")
st.subheader("Mata Kuliah Logika Pemrograman dan Komputer")

st.markdown("""
<div class="identitas-box">
    <span style="color: #0369a1; font-weight: bold; font-size: 1.05rem;">Kelompok 7:</span><br>
    <table style="width:100%; border:none; margin-top:5px; color:#334155; font-size:0.95rem;">
        <tr><td>1. 2560556 - AFFAN IHSANUL FATAH</td><td>2. 2560618 - ELVIA ELVARITTA</td></tr>
        <tr><td>3. 2560765 - MUHAMMAD AQIL</td><td>4. 2560739 - RAFI ALIFIA SHARIATI</td></tr>
        <tr><td>5. 2560796 - TIARA APRILIANTI</td><td></td></tr>
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
# MENU 1: BOBOT MOLEKUL (BM/Mr)
# ==========================================
if menu == "Bobot Molekul (BM/Mr)":
    st.header("🔬 Perhitungan Bobot Molekul")
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
                st.success(f"Bobot Molekul (BM) dari {input_senyawa} adalah: {format_koma(bm)} g/mol")
        else:
            st.warning("Silakan isi rumus kimia terlebih dahulu.")

# ==========================================
# MENU 2: KONVERSI SATUAN KIMIA
# ==========================================
elif menu == "Konversi Satuan Kimia":
    st.header("🔄 Konversi Hubungan Satuan Kimia")
    st.write("Silakan tentukan satuan awal dan satuan tujuan konversi yang Anda inginkan.")
    
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
    
    if satuan_asal == "Massa (gram)":
        g = st.number_input("Masukkan Nilai Massa (gram):", min_value=0.0, value=9.8)
        if satuan_tujuan in ["Molaritas (M)", "Normalitas (N)"]:
            v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=100.0)
        
        if st.button("Proses Konversi"):
            mol = g / mr_val
            if satuan_tujuan == "Mol (mol)":
                st.success(f"Hasil: {format_koma(g)} gram = {format_koma(mol)} mol")
            elif satuan_tujuan == "Molaritas (M)":
                molaritas = mol * (1000 / v_ml)
                st.success(f"Hasil: {format_koma(g)} gram dalam {format_koma_v(v_ml)} mL = {format_koma(molaritas)} M")
            elif satuan_tujuan == "Normalitas (N)":
                molaritas = mol * (1000 / v_ml)
                normalitas = molaritas * val_val
                st.success(f"Hasil: {format_koma(g)} gram dalam {format_koma_v(v_ml)} mL = {format_koma(normalitas)} N")

    elif satuan_asal == "Mol (mol)":
        mol = st.number_input("Masukkan Nilai Jumlah Mol (mol):", min_value=0.0, value=0.1)
        if satuan_tujuan in ["Molaritas (M)", "Normalitas (N)"]:
            v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=100.0)
        
        if st.button("Proses Konversi"):
            g = mol * mr_val
            if satuan_tujuan == "Massa (gram)":
                st.success(f"Hasil: {format_koma(mol)} mol = {format_koma(g)} gram")
            elif satuan_tujuan == "Molaritas (M)":
                molaritas = mol * (1000 / v_ml)
                st.success(f"Hasil: {format_koma(mol)} mol dalam {format_koma_v(v_ml)} mL = {format_koma(molaritas)} M")
            elif satuan_tujuan == "Normalitas (N)":
                molaritas = mol * (1000 / v_ml)
                normalitas = molaritas * val_val
                st.success(f"Hasil: {format_koma(mol)} mol dalam {format_koma_v(v_ml)} mL = {format_koma(normalitas)} N")

    elif satuan_asal == "Molaritas (M)":
        molaritas = st.number_input("Masukkan Nilai Molaritas (M):", min_value=0.0, value=1.0)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=250.0)
        
        if st.button("Proses Konversi"):
            g = (molaritas * mr_val * v_ml) / 1000
            mol = (molaritas * v_ml) / 1000
            normalitas = molaritas * val_val
            
            if satuan_tujuan == "Massa (gram)":
                st.success(f"Hasil: {format_koma(molaritas)} M dalam {format_koma_v(v_ml)} mL = {format_koma(g)} gram")
            elif satuan_tujuan == "Mol (mol)":
                st.success(f"Hasil: {format_koma(molaritas)} M dalam {format_koma_v(v_ml)} mL = {format_koma(mol)} mol")
            elif satuan_tujuan == "Normalitas (N)":
                st.success(f"Hasil: {format_koma(molaritas)} M = {format_koma(normalitas)} N")

    elif satuan_asal == "Normalitas (N)":
        normalitas = st.number_input("Masukkan Nilai Normalitas (N):", min_value=0.0, value=1.0)
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=250.0)
        
        if st.button("Proses Konversi"):
            molaritas = normalitas / val_val
            g = (molaritas * mr_val * v_ml) / 1000
            mol = (molaritas * v_ml) / 1000
            
            if satuan_tujuan == "Molaritas (M)":
                st.success(f"Hasil: {format_koma(normalitas)} N = {format_koma(molaritas)} M")
            elif satuan_tujuan == "Massa (gram)":
                st.success(f"Hasil: {format_koma(normalitas)} N dalam {format_koma_v(v_ml)} mL = {format_koma(g)} gram")
            elif satuan_tujuan == "Mol (mol)":
                st.success(f"Hasil: {format_koma(normalitas)} N dalam {format_koma_v(v_ml)} mL = {format_koma(mol)} mol")

# ==========================================
# MENU 3: FAKTOR PENGENCERAN
# ==========================================
elif menu == "Faktor Pengenceran":
    st.header("🧪 Perhitungan Pengenceran")
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
    
    if target_cari == "Konsentrasi Larutan Pekat (M1)":
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=10.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer Terbentuk (M2):", min_value=0.01, value=0.14)
        v2 = st.number_input("Masukkan Volume Larutan Encer Terbentuk (V2) dalam mL:", min_value=0.01, value=100.0)
        
        if st.button("Hitung M1"):
            m1 = (m2 * v2) / v1
            st.success(f"Hasil Perhitungan: Konsentrasi Larutan Pekat Asal (M1) = {format_koma(m1)} M (atau N)")
            
    elif target_cari == "Volume Larutan Pekat (V1)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=12.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.5)
        v2 = st.number_input("Masukkan Volume Larutan Encer yang Diinginkan (V2) dalam mL:", min_value=0.01, value=500.0)
        
        if st.button("Hitung V1"):
            if m1 >= m2:
                v1 = (m2 * v2) / m1
                st.success(f"Hasil Perhitungan: Ambil {format_koma(v1)} mL larutan pekat (V1), lalu encerkan hingga {format_koma_v(v2)} mL.")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari... (M2)!")

    elif target_cari == "Konsentrasi Larutan Encer (M2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=2.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=25.0)
        v2 = st.number_input("Masukkan Volume Larutan Setelah Diencerkan (V2) dalam mL:", min_value=0.01, value=250.0)
        
        if st.button("Hitung M2"):
            if v2 >= v1:
                m2 = (m1 * v1) / v2
                st.success(f"Hasil Perhitungan: Konsentrasi Larutan Setelah Diencerkan (M2) = {format_koma(m2)} M (atau N)")
            else:
                st.error("Gagal: Volume akhir (V2) harus lebih besar daripada volume awal (V1)!")

    elif target_cari == "Volume Larutan Encer (V2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=6.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=10.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.1)
        
        if st.button("Hitung V2"):
            if m1 >= m2:
                v2 = (m1 * v1) / m2
                st.success(f"Hasil Perhitungan: Volume Akhir Larutan Encer (V2) = {format_koma_v(v2)} mL")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari... (M2)!")

# --- FOOTER ---
st.markdown("---")
st.caption("Aplikasi Logika Pemrograman & Komputer | Kelompok 7 | © 2026")
