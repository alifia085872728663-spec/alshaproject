import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# --- REVISI TOTAL: BACKGROUND ANIMASI MOLEKUL & GLASSMORPHISM ---
st.markdown("""
    <style>
    /* 1. Background Utama dengan Gradasi Lab Kimia Modern */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%) !important;
        background-attachment: fixed !important;
        color: #f1f5f9;
    }

    /* 2. Animasi Partikel Molekul Bergerak di Latar Belakang */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.15;
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='%2338bdf8'%3E%3Ccircle cx='400' cy='400' r='15'/%3E%3Ccircle cx='200' cy='200' r='10'/%3E%3Ccircle cx='600' cy='200' r='12'/%3E%3Ccircle cx='300' cy='600' r='8'/%3E%3Ccircle cx='550' cy='550' r='14'/%3E%3Cline x1='400' y1='400' x2='200' y2='200' stroke='%2338bdf8' stroke-width='2'/%3E%3Cline x1='400' y1='400' x2='600' y2='200' stroke='%2338bdf8' stroke-width='2'/%3E%3Cline x1='400' y1='400' x2='300' y2='600' stroke='%2338bdf8' stroke-width='2'/%3E%3Cline x1='400' y1='400' x2='550' y2='550' stroke='%2338bdf8' stroke-width='2'/%3E%3C/g%3E%3C/svg%3E");
        background-size: 450px;
        animation: floatBackground 25s linear infinite;
    }

    @keyframes floatBackground {
        0% { background-position: 0px 0px; }
        100% { background-position: 450px 450px; }
    }
    
    .main .block-container {
        position: relative;
        z-index: 1;
    }
    
    /* 3. Desain Sidebar Transparan Elegan */
    div[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    /* 4. Pewarnaan Teks Judul (Glow Effect) */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }
    
    /* 5. Efek Kaca (Glassmorphism) untuk Kotak Identitas */
    .identitas-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-top: 10px;
        margin-bottom: 25px;
    }
    
    /* 6. Tombol Interaktif dengan Efek Transisi Warna */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        padding: 12px 0px;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
        background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%) !important;
    }

    /* Mengubah warna teks input bawaan streamlit agar kontras */
    label, p, span {
        color: #e2e8f0 !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE TABEL PERIODIK ---
AR_PERIODIK = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38, 'Ag': 107.87, 'I': 126.90, 'Ba': 137.33, 'Pb': 207.2
}

# --- FUNGSI FORMATTING INDONESIA ---
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
    rincian = []
    
    for unsur, jumlah in komponen.items():
        if unsur in AR_PERIODIK:
            ar_unsur = AR_PERIODIK[unsur]
            sub_total = ar_unsur * jumlah
            total_bm += sub_total
            rincian.append(f"({jumlah} \\times \\text{{Ar }} {unsur} [{format_koma(ar_unsur)}])")
        else:
            unsur_tidak_dikenal.append(unsur)
            
    cara_teks = " + ".join(rincian)
    return total_bm, unsur_tidak_dikenal, cara_teks

# ==========================================
# HALAMAN UTAMA (KOMPONEN PERMANEN)
# ==========================================
st.title("🧪 Kalkulator Kimia")
st.markdown("### Perhitungan Bobot Molekul, Konversi Satuan, dan Faktor Pengenceran")

st.markdown("""
<div class="identitas-box">
    <div style="color: #38bdf8; font-weight: bold; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; margin-bottom: 10px;">
        📄 INFORMASI PROJECT MAKALAH
    </div>
    <table style="width:100%; border:none; color:#cbd5e1; font-size:0.95rem; line-height: 1.6;">
        <tr><td style="width: 25%; font-weight: bold; color: #38bdf8;">Mata Kuliah</td><td>: Logika Pemrograman dan Komputer</td></tr>
        <tr><td style="font-weight: bold; color: #38bdf8;">Kelas</td><td style="color: #34d399; font-weight: bold;">: 1A</td></tr>
        <tr><td style="font-weight: bold; color: #38bdf8;">Kelompok</td><td>: Kelompok 7</td></tr>
        <tr><td style="vertical-align: top; font-weight: bold; color: #38bdf8;">Anggota</td><td>: 
            <table style="width:100%; margin-top:-2px; border:none; color:#cbd5e1;">
                <tr><td>• 2560556 - AFFAN IHSANUL FATAH</td><td>• 2560618 - ELVIA ELVARITTA</td></tr>
                <tr><td>• 2560765 - MUHAMMAD AQIL</td><td>• 2560739 - RAFI ALIFIA SHARIATI</td></tr>
                <tr><td>• 2560796 - TIARA APRILIANTI</td><td></td></tr>
            </table>
        </td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGASI MENU
# ==========================================
st.sidebar.header("🧭 Menu Fitur")
menu = st.sidebar.radio(
    "Silakan Pilih Fitur Perhitungan:",
    [
        "Silakan Pilih...",
        "1. Perhitungan Bobot Molekul (BM/Mr)", 
        "2. Konversi Satuan Kimia", 
        "3. Perhitungan Faktor Pengenceran"
    ]
)

st.markdown("---")

if menu == "Silakan Pilih...":
    st.info("💡 **Petunjuk Penggunaan:** Silakan gunakan **Menu Fitur** di sebelah kiri (sidebar) untuk memilih jenis kalkulator kimia yang ingin Anda operasikan.")

# ==========================================
# MENU 1: BOBOT MOLEKUL (BM/Mr)
# ==========================================
elif menu == "1. Perhitungan Bobot Molekul (BM/Mr)":
    st.header("🔬 Perhitungan Bobot Molekul")
    st.write("Ketik rumus molekul senyawa kimia secara langsung untuk mengetahui berat molekul beserta langkah detailnya.")
    
    input_senyawa = st.text_input("Masukkan Rumus Kimia Senyawa (Contoh: H2SO4, Ca(OH)2, NaCl):", "H2SO4")
    
    if st.button("Hitung BM / Mr"):
        if input_senyawa:
            bm, error_unsur, cara_teks = hitung_bm_dari_teks(input_senyawa)
            if error_unsur:
                st.error(f"Unsur tidak dikenal: {', '.join(error_unsur)}. Gunakan huruf besar di awal unsur (Contoh: 'NaOH' bukan 'naoh').")
            elif bm == 0:
                st.warning("Format rumus tidak valid.")
            else:
                st.success(f"Bobot Molekul (BM) dari {input_senyawa} adalah: {format_koma(bm)} g/mol")
                st.markdown("### 📝 Langkah Perhitungan Matematis:")
                st.latex(r"\text{Mr } \text{" + input_senyawa + r"} = \sum (\text{Jumlah Atom} \times \text{Ar})")
                st.latex(r"\text{Mr } \text{" + input_senyawa + r"} = " + cara_teks)
                st.latex(r"\text{Hasil Akhir} = " + format_koma(bm) + r"\text{ g/mol}")
        else:
            st.warning("Silakan isi rumus kimia terlebih dahulu.")

# ==========================================
# MENU 2: KONVERSI SATUAN KIMIA
# ==========================================
elif menu == "2. Konversi Satuan Kimia":
    st.header("🔄 Konversi Hubungan Satuan Kimia")
    st.write("Tentukan satuan awal dan tujuan konversi. Fitur ini mendukung konversi Massa, Mol, Molaritas, Normalitas, ppm, dan Persen Bobot.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        mr_val = st.number_input("Massa Molar / Mr Senyawa (g/mol):", min_value=0.1, value=98.0, step=0.1)
    with c2:
        val_val = st.number_input("Valensi / Ekivalen Zat (n):", min_value=1, value=2, step=1)
    with c3:
        rho_val = st.number_input("Massa Jenis Larutan / ρ (g/mL):", min_value=0.01, value=1.0, step=0.01)
        
    st.markdown("### ⚙️ Pengaturan Alur Konversi")
    
    daftar_satuan = [
        "Massa (gram)", "Mol (mol)", "Molaritas (M)", 
        "Normalitas (N)", "Part Per Million (ppm)", "Persen Bobot (% b/b)"
    ]
    
    col_from, col_to = st.columns(2)
    with col_from:
        satuan_asal = st.selectbox("Pilih Satuan Asal (Yang Diketahui):", daftar_satuan, index=5)
    with col_to:
        daftar_tujuan = daftar_satuan.copy()
        if satuan_asal in daftar_tujuan:
            daftar_tujuan.remove(satuan_asal)
        satuan_tujuan = st.selectbox("Pilih Satuan Tujuan (Yang Dicari):", daftar_tujuan, index=4)

    st.markdown("---")
    
    nilai_asal = st.number_input(f"Masukkan Nilai dari {satuan_asal}:", min_value=0.0, value=0.05, format="%.4f", step=0.01)
    
    butuh_volume = [
        ("Massa (gram)", "Molaritas (M)"), ("Massa (gram)", "Normalitas (N)"), ("Massa (gram)", "Part Per Million (ppm)"),
        ("Mol (mol)", "Molaritas (M)"), ("Mol (mol)", "Normalitas (N)"), ("Mol (mol)", "Part Per Million (ppm)"),
        ("Molaritas (M)", "Massa (gram)"), ("Molaritas (M)", "Mol (mol)"),
        ("Normalitas (N)", "Massa (gram)"), ("Normalitas (N)", "Mol (mol)"),
        ("Part Per Million (ppm)", "Massa (gram)"), ("Part Per Million (ppm)", "Mol (mol)")
    ]
    
    v_ml = 1000.0
    if (satuan_asal, satuan_tujuan) in butuh_volume or (satuan_tujuan, satuan_asal) in butuh_volume:
        v_ml = st.number_input("Masukkan Volume Larutan (mL):", min_value=0.1, value=1000.0, step=50.0)

    if st.button("Proses Konversi Satuan"):
        st.markdown("### 📝 Langkah Perhitungan Analisis Dimensi:")
        hasil_akhir = 0.0
        
        if satuan_asal == "Persen Bobot (% b/b)" and satuan_tujuan == "Part Per Million (ppm)":
            hasil_akhir = nilai_asal * 10000
            st.markdown("**1. Mengubah Persen Bobot (% b/b) langsung ke Part Per Million (ppm):**")
            st.latex(r"\text{ppm} = \% \text{ b/b} \times 10.000")
            st.latex(r"\text{ppm} = " + format_koma(nilai_asal) + r"\% \times 10.000 = " + format_koma(hasil_akhir) + r"\text{ ppm}")
            
        elif satuan_asal == "Part Per Million (ppm)" and satuan_tujuan == "Persen Bobot (% b/b)":
            hasil_akhir = nilai_asal / 10000
            st.markdown("**1. Mengubah Part Per Million (ppm) langsung ke Persen Bobot (% b/b):**")
            st.latex(r"\% \text{ b/b} = \frac{\text{ppm}}{10.000}")
            st.latex(r"\% \text{ b/b} = \frac{" + format_koma(nilai_asal) + r"\text{ ppm}}{10.000} = " + format_koma(hasil_akhir) + r"\%")
            
        else:
            molaritas_pusat = 0.0
            st.markdown("**1. Konversi Satuan Asal ke Molaritas Pusat (M):**")
            
            if satuan_asal == "Molaritas (M)":
                molaritas_pusat = nilai_asal
                st.latex(r"\text{Molaritas Pusat (M)} = " + format_koma(molaritas_pusat) + r"\text{ mol/L}")
            elif satuan_asal == "Massa (gram)":
                molaritas_pusat = (nilai_asal / mr_val) * (1000 / v_ml)
                st.latex(r"M = \frac{\text{gram}}{\text{Mr}} \times \frac{1000 \text{ mL/L}}{V_{\text{mL}}}")
                st.latex(r"M = \frac{" + format_koma(nilai_asal) + r"\text{ g}}{" + format_koma(mr_val) + r"\text{ g/mol}} \times \frac{1000 \text{ mL/L}}{" + format_koma_v(v_ml) + r"\text{ mL}} = " + format_koma(molaritas_pusat) + r"\text{ mol/L (M)}")
            elif satuan_asal == "Mol (mol)":
                molaritas_pusat = nilai_asal * (1000 / v_ml)
                st.latex(r"M = \text{mol} \times \frac{1000 \text{ mL/L}}{V_{\text{mL}}}")
                st.latex(r"M = " + format_koma(nilai_asal) + r"\text{ mol} \times \frac{1000 \text{ mL/L}}{" + format_koma_v(v_ml) + r"\text{ mL}} = " + format_koma(molaritas_pusat) + r"\text{ mol/L (M)}")
            elif satuan_asal == "Normalitas (N)":
                molaritas_pusat = nilai_asal / val_val
                st.latex(r"M = \frac{N}{\text{Valensi}}")
                st.latex(r"M = \frac{" + format_koma(nilai_asal) + r"\text{ ekv/L}}{" + str(val_val) + r"\text{ ekv/mol}} = " + format_koma(molaritas_pusat) + r"\text{ mol/L (M)}")
            elif satuan_asal == "Part Per Million (ppm)":
                molaritas_pusat = nilai_asal / (mr_val * 1000)
                st.latex(r"M = \frac{\text{ppm}}{\text{Mr} \times 1000 \text{ mg/g}}")
                st.latex(r"M = \frac{" + format_koma(nilai_asal) + r"\text{ mg/L}}{" + format_koma(mr_val) + r"\text{ g/mol} \times 1000 \text{ mg/g}} = " + format_koma(molaritas_pusat) + r"\text{ mol/L (M)}")
            elif satuan_asal == "Persen Bobot (% b/b)":
                molaritas_pusat = (nilai_asal * rho_val * 10) / mr_val
                st.latex(r"M = \frac{\% \times \rho \times 10 \text{ mL}\cdot\%/\text{L}}{\text{Mr}}")
                st.latex(r"M = \frac{" + format_koma(nilai_asal) + r"\% \times " + format_koma(rho_val) + r"\text{ g/mL} \times 10 \text{ mL}\cdot\%/\text{L}}{" + format_koma(mr_val) + r"\text{ g/mol}} = " + format_koma(molaritas_pusat) + r"\text{ mol/L (M)}")

            st.markdown("**2. Konversi Molaritas Pusat (M) ke Satuan Target:**")
            if satuan_tujuan == "Molaritas (M)":
                hasil_akhir = molaritas_pusat
                st.latex(r"\text{Hasil Akhir} = " + format_koma(hasil_akhir) + r"\text{ mol/L (M)}")
            elif satuan_tujuan == "Massa (gram)":
                hasil_akhir = (molaritas_pusat * mr_val * v_ml) / 1000
                st.latex(r"\text{gram} = \frac{M \times \text{Mr} \times V_{\text{mL}}}{1000 \text{ mL/L}}")
                st.latex(r"\text{gram} = \frac{" + format_koma(molaritas_pusat) + r"\text{ mol/L} \times " + format_koma(mr_val) + r"\text{ g/mol} \times " + format_koma_v(v_ml) + r"\text{ mL}}{1000 \text{ mL/L}} = " + format_koma(hasil_akhir) + r"\text{ gram}")
            elif satuan_tujuan == "Mol (mol)":
                hasil_akhir = (molaritas_pusat * v_ml) / 1000
                st.latex(r"\text{mol} = \frac{M \times V_{\text{mL}}}{1000 \text{ mL/L}}")
                st.latex(r"\text{mol} = \frac{" + format_koma(molaritas_pusat) + r"\text{ mol/L} \times " + format_koma_v(v_ml) + r"\text{ mL}}{1000 \text{ mL/L}} = " + format_koma(hasil_akhir) + r"\text{ mol}")
            elif satuan_tujuan == "Normalitas (N)":
                hasil_akhir = molaritas_pusat * val_val
                st.latex(r"N = M \times \text{Valensi}")
                st.latex(r"N = " + format_koma(molaritas_pusat) + r"\text{ mol/L} \times " + str(val_val) + r"\text{ ekv/mol} = " + format_koma(hasil_akhir) + r"\text{ ekv/L (N)}")
            elif satuan_tujuan == "Part Per Million (ppm)":
                hasil_akhir = molaritas_pusat * mr_val * 1000
                st.latex(r"\text{ppm} = M \times \text{Mr} \times 1000 \text{ mg/g}")
                st.latex(r"\text{ppm} = " + format_koma(molaritas_pusat) + r"\text{ mol/L} \times " + format_koma(mr_val) + r"\text{ g/mol} \times 1000 \text{ mg/g} = " + format_koma(hasil_akhir) + r"\text{ mg/L (ppm)}")
            elif satuan_tujuan == "Persen Bobot (% b/b)":
                hasil_akhir = (molaritas_pusat * mr_val) / (rho_val * 10)
                st.latex(r"\% \text{ b/b} = \frac{M \times \text{Mr}}{\rho \times 10 \text{ mL}\cdot\%/\text{L}}")
                st.latex(r"\% \text{ b/b} = \frac{" + format_koma(molaritas_pusat) + r"\text{ mol/L} \times " + format_koma(mr_val) + r"\text{ g/mol}}{" + format_koma(rho_val) + r"\text{ g/mL} \times 10 \text{ mL}\cdot\%/\text{L}} = " + format_koma(hasil_akhir) + r"\%")

        st.success(f"Hasil Akhir Konversi: {format_koma(nilai_asal)} {satuan_asal} = {format_koma(hasil_akhir)} {satuan_tujuan}")

# ==========================================
# MENU 3: FAKTOR PENGENCERAN
# ==========================================
elif menu == "3. Perhitungan Faktor Pengenceran":
    st.header("🧪 Perhitungan Pengenceran Larutan")
    st.write("Gunakan prinsip stoikiometri pengenceran murni berbasis hukum kekekalan mol: $V_1 \\times M_1 = V_2 \\times M_2$")
    
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
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer Terbentuk (M2) dalam M (atau N):", min_value=0.01, value=0.14)
        v2 = st.number_input("Masukkan Volume Larutan Encer Terbentuk (V2) dalam mL:", min_value=0.01, value=100.0)
        
        if st.button("Hitung M1"):
            m1 = (m2 * v2) / v1
            st.markdown("### 📝 Langkah Perhitungan:")
            st.latex(r"V_1 \times M_1 = V_2 \times M_2")
            st.latex(r"M_1 = \frac{V_2 \times M_2}{V_1}")
            st.latex(r"M_1 = \frac{" + format_koma_v(v2) + r"\text{ mL} \times " + format_koma(m2) + r"\text{ M}}{" + format_koma_v(v1) + r"\text{ mL}} = " + format_koma(m1) + r"\text{ M}")
            st.success(f"Hasil Akhir: Konsentrasi Larutan Pekat Asal (M1) = {format_koma(m1)} M (atau N)")
            
    elif target_cari == "Volume Larutan Pekat (V1)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1) dalam M (atau N):", min_value=0.01, value=12.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2) dalam M (atau N):", min_value=0.01, value=0.5)
        v2 = st.number_input("Masukkan Volume Larutan Encer yang Diinginkan (V2) dalam mL:", min_value=0.01, value=500.0)
        
        if st.button("Hitung V1"):
            if m1 >= m2:
                v1 = (m2 * v2) / m1
                st.markdown("### 📝 Langkah Perhitungan:")
                st.latex(r"V_1 \times M_1 = V_2 \times M_2")
                st.latex(r"V_1 = \frac{V_2 \times M_2}{M_1}")
                st.latex(r"V_1 = \frac{" + format_koma_v(v2) + r"\text{ mL} \times " + format_koma(m2) + r"\text{ M}}{" + format_koma(m1) + r"\text{ M}} = " + format_koma(v1) + r"\text{ mL}")
                st.success(f"Hasil Akhir: Ambil {format_koma(v1)} mL larutan pekat (V1), lalu encerkan hingga {format_koma_v(v2)} mL.")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari konsentrasi akhir (M2)!")

    elif target_cari == "Konsentrasi Larutan Encer (M2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1) dalam M (atau N):", min_value=0.01, value=2.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=25.0)
        v2 = st.number_input("Masukkan Volume Larutan Setelah Diencerkan (V2) dalam mL:", min_value=0.01, value=250.0)
        
        if st.button("Hitung M2"):
            if v2 >= v1:
                m2 = (m1 * v1) / v2
                st.markdown("### 📝 Langkah Perhitungan:")
                st.latex(r"V_1 \times M_1 = V_2 \times M_2")
                st.latex(r"M_2 = \frac{V_1 \times M_1}{V_2}")
                st.latex(r"M_2 = \frac{" + format_koma_v(v1) + r"\text{ mL} \times " + format_koma(m1) + r"\text{ M}}{" + format_koma_v(v2) + r"\text{ mL}} = " + format_koma(m2) + r"\text{ M}")
                st.success(f"Hasil Akhir: Konsentrasi Larutan Setelah Diencerkan (M2) = {format_koma(m2)} M (atau N)")
            else:
                st.error("Gagal: Volume akhir (V2) harus lebih besar daripada volume awal (V1)!")

    elif target_cari == "Volume Larutan Encer (V2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1) dalam M (atau N):", min_value=0.01, value=6.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=10.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2) dalam M (atau N):", min_value=0.01, value=0.1)
        
        if st.button("Hitung V2"):
            if m1 >= m2:
                v2 = (m1 * v1) / m2
                st.markdown("### 📝 Langkah Perhitungan:")
                st.latex(r"V_1 \times M_1 = V_2 \times M_2")
                st.latex(r"V_2 = \frac{V_1 \times M_1}{M_2}")
                st.latex(r"V_2 = \frac{" + format_koma_v(v1) + r"\text{ mL} \times " + format_koma(m1) + r"\text{ M}}{" + format_koma(m2) + r"\text{ M}} = " + format_koma_v(v2) + r"\text{ mL}")
                st.success(f"Hasil Akhir: Volume Akhir Larutan Encer (V2) = {format_koma_v(v2)} mL")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari konsentrasi akhir (M2)!")

# --- FOOTER ---
st.markdown("---")
st.caption("Aplikasi Logika Pemrograman & Komputer | Kelas 1A - Kelompok 7 | ©️ 2026")
