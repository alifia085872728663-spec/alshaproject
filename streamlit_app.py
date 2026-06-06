import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia - Kelompok 7",
    page_icon="🧪",
    layout="centered"
)

# --- REVISI TOTAL: GRADASI & ELEMEN KIMIA MURNI CSS/SVG ---
st.markdown("""
    <style>
    /* Background dengan gradasi warna Lembut: Biru -> Putih -> Kuning */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #ffffff 50%, #fef9c3 100%) !important;
        background-attachment: fixed !important;
        color: #1e293b;
    }

    /* Elemen Grafis Kimia Transparan Langsung via SVG */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.08;
        z-index: 0;
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%230284c7' stroke-width='3'%3E%3Cpath d='M80 650 L140 650 L120 530 L100 530 Z' /%3E%3Cpath d='M100 560 L140 560 M105 590 L135 590 M110 620 L130 620' /%3E%3Ccircle cx='190' cy='520' r='12' /%3E%3Ccircle cx='250' cy='490' r='18' /%3E%3Ccircle cx='290' cy='540' r='10' /%3E%3Cline x1='190' y1='520' x2='235' y2='495' /%3E%3Cline x1='250' y1='490' x2='290' y2='530' /%3E%3C/g%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%230369a1' stroke-width='2.5'%3E%3Cpath d='M680 150 L680 190 L630 300 L730 300 L680 190' /%3E%3Cpath d='M645 270 L715 270 M655 240 L705 240' /%3E%3Cpolygon points='600,100 640,80 680,100 680,140 640,160 600,140' /%3E%3Cpolygon points='560,140 600,160 600,200 560,220 520,200 520,140' /%3E%3C/g%3E%3C/svg%3E");
        background-position: left bottom, right top;
        background-repeat: no-repeat;
        background-size: 380px, 380px;
    }
    
    .main .block-container {
        position: relative;
        z-index: 1;
    }
    
    div[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-right: 1px solid #e2e8f0;
    }
    
    h1, h2, h3 {
        color: #0369a1 !important;
        font-weight: 700;
    }
    
    .identitas-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #0ea5e9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 10px;
        margin-bottom: 25px;
    }
    
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
            rincian.append(f"({jumlah} x Ar {unsur} [{format_koma(ar_unsur)}])")
        else:
            unsur_tidak_dikenal.append(unsur)
            
    cara_teks = " + ".join(rincian)
    return total_bm, unsur_tidak_dikenal, cara_teks

# ==========================================
# HALAMAN UTAMA (SELALU MUNCUL DI ATAS)
# ==========================================
st.title("🧪 Kalkulator Kimia")
st.markdown("### Perhitungan Bobot Molekul, Konversi Satuan, dan Faktor Pengenceran")

st.markdown("""
<div class="identitas-box">
    <div style="color: #0369a1; font-weight: bold; font-size: 1.1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; margin-bottom: 10px;">
        📄 INFORMASI PROJECT MAKALAH
    </div>
    <table style="width:100%; border:none; color:#334155; font-size:0.95rem; line-height: 1.6;">
        <tr><td style="width: 25%; font-weight: bold;">Mata Kuliah</td><td>: Logika Pemrograman dan Komputer</td></tr>
        <tr><td style="font-weight: bold;">Kelompok</td><td>: Kelompok 7</td></tr>
        <tr><td style="vertical-align: top; font-weight: bold;">Anggota</td><td>: 
            <table style="width:100%; margin-top:-2px; border:none; color:#334155;">
                <tr><td>• 2560556 - AFFAN IHSANUL FATAH</td><td>• 2560618 - ELVIA ELVARITTA</td></tr>
                <tr><td>• 2560765 - MUHAMMAD AQIL</td><td>• 2560739 - RAFI ALIFIA SHARIATI</td></tr>
                <tr><td>• 2560796 - TIARA APRILIANTI</td><td></td></tr>
            </table>
        </td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGASI MENU (3 POIN UTAMA)
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

# ==========================================
# KONDISI JIKA BELUM MEMILIH MENU
# ==========================================
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
                
                st.markdown("### 📝 Langkah Perhitungan:")
                st.info(f"**Rumus:** Mr = Σ (Jumlah Atom x Ar)\n\n"
                        f"**Proses Hitung:**\n"
                        f"Mr {input_senyawa} = {cara_teks}\n\n"
                        f"**Hasil Akhir:** {format_koma(bm)} g/mol")
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
        satuan_asal = st.selectbox("Pilih Satuan Asal (Yang Diketahui):", daftar_satuan, index=2)
    with col_to:
        daftar_tujuan = daftar_satuan.copy()
        if satuan_asal in daftar_tujuan:
            daftar_tujuan.remove(satuan_asal)
        satuan_tujuan = st.selectbox("Pilih Satuan Tujuan (Yang Dicari):", daftar_tujuan, index=2)

    st.markdown("---")
    
    nilai_asal = st.number_input(f"Masukkan Nilai dari {satuan_asal}:", min_value=0.0, value=1.0, step=0.1)
    
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
        molaritas_pusat = 0.0
        langkah_ke_molaritas = ""
        
        if satuan_asal == "Molaritas (M)":
            molaritas_pusat = nilai_asal
            langkah_ke_molaritas = f"Satuan asal sudah dalam Molaritas = {format_koma(molaritas_pusat)} M."
        elif satuan_asal == "Massa (gram)":
            molaritas_pusat = (nilai_asal / mr_val) * (1000 / v_ml)
            langkah_ke_molaritas = f"1. Mengubah Massa ke Molaritas:\n   M = (gram / Mr) * (1000 / V_mL)\n   M = ({format_koma(nilai_asal)} / {format_koma(mr_val)}) * (1000 / {format_koma_v(v_ml)}) = {format_koma(molaritas_pusat)} M"
        elif satuan_asal == "Mol (mol)":
            molaritas_pusat = nilai_asal * (1000 / v_ml)
            langkah_ke_molaritas = f"1. Mengubah Mol ke Molaritas:\n   M = mol * (1000 / V_mL)\n   M = {format_koma(nilai_asal)} * (1000 / {format_koma_v(v_ml)}) = {format_koma(molaritas_pusat)} M"
        elif satuan_asal == "Normalitas (N)":
            molaritas_pusat = nilai_asal / val_val
            langkah_ke_molaritas = f"1. Mengubah Normalitas ke Molaritas:\n   M = N / Valensi\n   M = {format_koma(nilai_asal)} / {val_val} = {format_koma(molaritas_pusat)} M"
        elif satuan_asal == "Part Per Million (ppm)":
            molaritas_pusat = nilai_asal / (mr_val * 1000)
            langkah_ke_molaritas = f"1. Mengubah ppm ke Molaritas:\n   M = ppm / (Mr * 1000)\n   M = {format_koma(nilai_asal)} / ({format_koma(mr_val)} * 1000) = {format_koma(molaritas_pusat)} M"
        elif satuan_asal == "Persen Massa (% b/b)":
            molaritas_pusat = (nilai_asal * rho_val * 10) / mr_val
            langkah_ke_molaritas = f"1. Mengubah % b/b ke Molaritas:\n   M = (% * ρ * 10) / Mr\n   M = ({format_koma(nilai_asal)} * {format_koma(rho_val)} * 10) / {format_koma(mr_val)} = {format_koma(molaritas_pusat)} M"

        hasil_akhir = 0.0
        langkah_ke_tujuan = ""
        
        if satuan_tujuan == "Molaritas (M)":
            hasil_akhir = molaritas_pusat
            langkah_ke_tujuan = f"2. Satuan target adalah Molaritas = {format_koma(hasil_akhir)} M"
        elif satuan_tujuan == "Massa (gram)":
            hasil_akhir = (molaritas_pusat * mr_val * v_ml) / 1000
            langkah_ke_tujuan = f"2. Mengubah Molaritas ke Massa:\n   gram = (M * Mr * V_mL) / 1000\n   gram = ({format_koma(molaritas_pusat)} * {format_koma(mr_val)} * {format_koma_v(v_ml)}) / 1000 = {format_koma(hasil_akhir)} gram"
        elif satuan_tujuan == "Mol (mol)":
            hasil_akhir = (molaritas_pusat * v_ml) / 1000
            langkah_ke_tujuan = f"2. Mengubah Molaritas ke Jumlah Mol:\n   mol = (M * V_mL) / 1000\n   mol = ({format_koma(molaritas_pusat)} * {format_koma_v(v_ml)}) / 1000 = {format_koma(hasil_akhir)} mol"
        elif satuan_tujuan == "Normalitas (N)":
            hasil_akhir = molaritas_pusat * val_val
            langkah_ke_tujuan = f"2. Mengubah Molaritas ke Normalitas:\n   N = M * Valensi\n   N = {format_koma(molaritas_pusat)} * {val_val} = {format_koma(hasil_akhir)} N"
        elif satuan_tujuan == "Part Per Million (ppm)":
            hasil_akhir = molaritas_pusat * mr_val * 1000
            langkah_ke_tujuan = f"2. Mengubah Molaritas ke ppm:\n   ppm = M * Mr * 1000\n   ppm = {format_koma(molaritas_pusat)} * {format_koma(mr_val)} * 1000 = {format_koma(hasil_akhir)} ppm"
        elif satuan_tujuan == "Persen Massa (% b/b)":
            hasil_akhir = (molaritas_pusat * mr_val) / (rho_val * 10)
            langkah_ke_tujuan = f"2. Mengubah Molaritas ke % b/b:\n   % b/b = (M * Mr) / (ρ * 10)\n   % b/b = ({format_koma(molaritas_pusat)} * {format_koma(mr_val)}) / ({format_koma(rho_val)} * 10) = {format_koma(hasil_akhir)} %"

        st.success(f"Hasil Konversi: {format_koma(nilai_asal)} {satuan_asal} = {format_koma(hasil_akhir)} {satuan_tujuan}")
        
        st.markdown("### 📝 Langkah Perhitungan Berdasarkan Alur Logika:")
        st.info(f"{langkah_ke_molaritas}\n\n{langkah_ke_tujuan}")

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
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer Terbentuk (M2):", min_value=0.01, value=0.14)
        v2 = st.number_input("Masukkan Volume Larutan Encer Terbentuk (V2) dalam mL:", min_value=0.01, value=100.0)
        
        if st.button("Hitung M1"):
            m1 = (m2 * v2) / v1
            st.success(f"Hasil Perhitungan: Konsentrasi Larutan Pekat Asal (M1) = {format_koma(m1)} M (atau N)")
            
            st.markdown("### 📝 Langkah Perhitungan:")
            st.info(f"**Rumus Dasar:** V1 * M1 = V2 * M2\n\n"
                    f"**Turunan Rumus:** M1 = (M2 * V2) / V1\n\n"
                    f"**Proses Hitung:** M1 = ({format_koma(m2)} * {format_koma_v(v2)}) / {format_koma_v(v1)}\n\n"
                    f"**Hasil Akhir:** {format_koma(m1)} M")
            
    elif target_cari == "Volume Larutan Pekat (V1)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=12.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.5)
        v2 = st.number_input("Masukkan Volume Larutan Encer yang Diinginkan (V2) dalam mL:", min_value=0.01, value=500.0)
        
        if st.button("Hitung V1"):
            if m1 >= m2:
                v1 = (m2 * v2) / m1
                st.success(f"Hasil Perhitungan: Ambil {format_koma(v1)} mL larutan pekat (V1), lalu encerkan hingga {format_koma_v(v2)} mL.")
                
                st.markdown("### 📝 Langkah Perhitungan:")
                st.info(f"**Rumus Dasar:** V1 * M1 = V2 * M2\n\n"
                        f"**Turunan Rumus:** V1 = (M2 * V2) / M1\n\n"
                        f"**Proses Hitung:** V1 = ({format_koma(m2)} * {format_koma_v(v2)}) / {format_koma(m1)}\n\n"
                        f"**Hasil Akhir:** Ambil {format_koma(v1)} mL larutan pekat, tambahkan aquadest hingga volume total {format_koma_v(v2)} mL.")
            else:
                st.error("Gagal: Konsentrasi awal (M1) tidak boleh lebih kecil dari konsentrasi akhir (M2)!")

    elif target_cari == "Konsentrasi Larutan Encer (M2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=2.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=25.0)
        v2 = st.number_input("Masukkan Volume Larutan Setelah Diencerkan (V2) dalam mL:", min_value=0.01, value=250.0)
        
        if st.button("Hitung M2"):
            if v2 >= v1:
                m2 = (m1 * v1) / v2
                st.success(f"Hasil Perhitungan: Konsentrasi Larutan Setelah Diencerkan (M2) = {format_koma(m2)} M (atau N)")
                
                st.markdown("### 📝 Langkah Perhitungan:")
                st.info(f"**Rumus Dasar:** V1 * M1 = V2 * M2\n\n"
                        f"**Turunan Rumus:** M2 = (M1 * V1) / V2\n\n"
                        f"**Proses Hitung:** M2 = ({format_koma(m1)} * {format_koma_v(v1)}) / {format_koma_v(v2)}\n\n"
                        f"**Hasil Akhir:** {format_koma(m2)} M")
            else:
                st.error("Gagal: Volume akhir (V2) harus lebih besar daripada volume awal (V1)!")

    elif target_cari == "Volume Larutan Encer (V2)":
        m1 = st.number_input("Masukkan Konsentrasi Larutan Pekat Asal (M1):", min_value=0.01, value=6.0)
        v1 = st.number_input("Masukkan Volume Larutan Pekat yang diambil (V1) dalam mL:", min_value=0.01, value=10.0)
        m2 = st.number_input("Masukkan Konsentrasi Larutan Encer yang Diinginkan (M2):", min_value=0.01, value=0.1)
        
        if st.button("Hitung V2"):
            if m1 >= m2:
                v2 = (m1 * v1) / m2
                st
