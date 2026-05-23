import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Kimia",
    page_icon="🧪",
    layout="centered"
)

# --- JUDUL UTAMA ---
st.title("🧪 Aplikasi Web Perhitungan Kimia")
st.write("Selamat datang di aplikasi pembantu laboratorium untuk tugas akhir Anda.")

# --- SIDEBAR NAVIGASI ---
st.sidebar.header("Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Fitur Perhitungan:",
    ["Bobot Molekul", "Konversi Satuan Kimia", "Faktor Pengenceran"]
)

# ==========================================
# FEATURE 1: PERHITUNGAN BOBOT MOLEKUL (BM)
# ==========================================
if menu == "Bobot Molekul":
    st.header("🧮 Perhitungan Bobot Molekul (BM)")
    st.write("Masukkan jumlah masing-masing atom untuk menghitung total Berat Molekul (g/mol).")
    
    # Tabel periodik sederhana (Ar) untuk demo dasar
    # Anda bisa memperluas ini sesuai kebutuhan
    Ar_dict = {
        'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999, 
        'Na': 22.990, 'Cl': 35.453, 'S': 32.065, 'K': 39.098
    }
    
    st.subheader("Masukkan Jumlah Atom:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        c_count = st.number_input("Jumlah Karbon (C)", min_value=0, value=0, step=1)
        h_count = st.number_input("Jumlah Hidrogen (H)", min_value=0, value=0, step=1)
    with col2:
        o_count = st.number_input("Jumlah Oksigen (O)", min_value=0, value=0, step=1)
        n_count = st.number_input("Jumlah Nitrogen (N)", min_value=0, value=0, step=1)
    with col3:
        na_count = st.number_input("Jumlah Natrium (Na)", min_value=0, value=0, step=1)
        cl_count = st.number_input("Jumlah Klorida (Cl)", min_value=0, value=0, step=1)

    # Logika Hitung
    if st.button("Hitung BM"):
        total_bm = (
            (c_count * Ar_dict['C']) + 
            (h_count * Ar_dict['H']) + 
            (o_count * Ar_dict['O']) + 
            (n_count * Ar_dict['N']) +
            (na_count * Ar_dict['Na']) +
            (cl_count * Ar_dict['Cl'])
        )
        
        if total_bm > 0:
            st.success(f"Hasil Perhitungan: **{total_bm:.4f} g/mol**")
            
            # Contoh rumus molekul sederhana yang terbentuk
            rumus = ""
            if c_count > 0: rumus += f"C{c_count}"
            if h_count > 0: rumus += f"H{h_count}"
            if n_count > 0: rumus += f"N{n_count}"
            if o_count > 0: rumus += f"O{o_count}"
            if na_count > 0: rumus += f"Na{na_count}"
            if cl_count > 0:  rumus += f"Cl{cl_count}"
            st.info(f"Estimasi rumus komponen: {rumus}")
        else:
            st.warning("Silakan masukkan jumlah atom terlebih dahulu.")

# ==========================================
# FEATURE 2: KONVERSI SATUAN KIMIA
# ==========================================
elif menu == "Konversi Satuan Kimia":
    st.header("🔄 Konversi Satuan Kimia (Mol ke Massa)")
    st.write("Fitur untuk mengubah jumlah zat (Mol) menjadi Massa (Gram) atau sebaliknya.")
    
    opsi_konversi = st.selectbox(
        "Pilih Arah Konversi:",
        ["Mol ke Gram (Massa)", "Gram (Massa) ke Mol"]
    )
    
    bm_senyawa = st.number_input("Masukkan BM / Mr Senyawa (g/mol):", min_value=0.1, value=58.5, step=0.1)
    
    if opsi_konversi == "Mol ke Gram (Massa)":
        nilai_mol = st.number_input("Masukkan Jumlah Mol:", min_value=0.0, value=1.0, step=0.1)
        if st.button("Konversi ke Gram"):
            hasil_gram = nilai_mol * bm_senyawa
            st.success(f"{nilai_mol} mol = **{hasil_gram:.4f} Gram**")
            
    elif opsi_konversi == "Gram (Massa) ke Mol":
        nilai_gram = st.number_input("Masukkan Massa (Gram):", min_value=0.0, value=10.0, step=0.1)
        if st.button("Konversi ke Mol"):
            hasil_mol = nilai_gram / bm_senyawa
            st.success(f"{nilai_gram} gram = **{hasil_mol:.4f} Mol**")

# ==========================================
# FEATURE 3: FAKTOR PENGENCERAN
# ==========================================
elif menu == "Faktor Pengenceran":
    st.header("🧪 Perhitungan Faktor Pengenceran (M1 . V1 = M2 . V2)")
    st.write("Hitung volume stock atau konsentrasi akhir menggunakan rumus pengenceran baku.")
    
    # Memilih apa yang ingin dicari user
    target_cari = st.selectbox(
        "Apa yang ingin Anda cari?",
        [
            "Volume Larutan Pekat yang Diperlukan (V1)", 
            "Konsentrasi Larutan Setelah Diencerkan (M2)"
        ]
    )
    
    if target_cari == "Volume Larutan Pekat yang Diperlukan (V1)":
        m1 = st.number_input("Konsentrasi Larutan Stok / Pekat (M1):", min_value=0.01, value=1.0, step=0.1)
        m2 = st.number_input("Konsentrasi yang Diinginkan (M2):", min_value=0.01, value=0.1, step=0.01)
        v2 = st.number_input("Volume Akhir yang Diinginkan (V2 dalam mL):", min_value=1.0, value=100.0, step=1.0)
        
        if st.button("Hitung V1"):
            if m1 >= m2:
                v1 = (m2 * v2) / m1
                faktor = m1 / m2
                st.success(f"Ambil **{v1:.2f} mL** larutan stok, lalu tambahkan aquades hingga total volume **{v2} mL**.")
                st.info(f"Faktor Pengenceran senyawa ini adalah **{faktor:.1f} kali**.")
            else:
                st.error("Error: Konsentrasi stok (M1) harus lebih besar dari konsentrasi akhir (M2)!")
                
    elif target_cari == "Konsentrasi Larutan Setelah Diencerkan (M2)":
        m1 = st.number_input("Konsentrasi Larutan Stok (M1):", min_value=0.01, value=1.0, step=0.1)
        v1 = st.number_input("Volume Larutan Stok yang Diambil (V1 dalam mL):", min_value=0.1, value=10.0, step=0.1)
        v2 = st.number_input("Volume Akhir Setelah Ditambah Pelarut (V2 dalam mL):", min_value=1.0, value=100.0, step=1.0)
        
        if st.button("Hitung M2"):
            if v2 >= v1:
                m2 = (m1 * v1) / v2
                faktor = v2 / v1
                st.success(f"Konsentrasi akhir larutan (M2) adalah: **{m2:.4f} M**")
                st.info(f"Faktor Pengenceran senyawa ini adalah **{faktor:.1f} kali**.")
            else:
                st.error("Error: Volume akhir (V2) harus lebih besar atau sama dengan volume awal (V1)!")

# --- FOOTER ---
st.markdown("---")
st.caption("Dibuat untuk memenuhi Tugas Akhir | © 2026")

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
