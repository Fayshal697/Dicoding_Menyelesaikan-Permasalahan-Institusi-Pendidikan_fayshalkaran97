import streamlit as st
import pandas as pd
import numpy as np
import joblib
import joblib

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jaya Jaya Institut – Prediksi Dropout",
    page_icon="🎓",
    layout="wide",
)

# ─── Load Artifacts ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model        = joblib.load("model\\model.joblib")
    scaler       = joblib.load("model\\scaler.pkl")
    feature_names = joblib.load("model\\feature_names.pkl")
    return model, scaler, feature_names

model, scaler, feature_names = load_artifacts()

# ─── Label Mappings (konsisten dengan notebook) ─────────────────────────────────
# Course: label -> kode numerik (untuk dikirim ke model)
COURSE_OPTIONS = {
    'Biofuel Production Technologies':   33,
    'Animation and Multimedia Design':   171,
    'Social Service (Evening)':          8014,
    'Agronomy':                          9003,
    'Communication Design':              9070,
    'Veterinary Nursing':                9085,
    'Informatics Engineering':           9119,
    'Equinculture':                      9130,
    'Management':                        9147,
    'Social Service':                    9238,
    'Tourism':                           9254,
    'Nursing':                           9500,
    'Oral Hygiene':                      9556,
    'Advertising & Marketing Mgmt':      9670,
    'Journalism and Communication':      9773,
    'Basic Education':                   9853,
    'Management (Evening)':              9991,
}

# Gender: label -> kode numerik
GENDER_OPTIONS = {'Female': 0, 'Male': 1}

# Scholarship holder: label -> kode numerik
SCHOLARSHIP_OPTIONS = {'No': 0, 'Yes': 1}

# Binary Yes/No options (untuk kolom lain)
YES_NO = {'No': 0, 'Yes': 1}

# SPP / Tuition
TUITION_OPTIONS = {'In Arrears': 0, 'Up to Date': 1}

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=80)
    st.title("Jaya Jaya Institut")
    st.caption("Sistem Deteksi Dini Dropout Mahasiswa")
    st.divider()
    st.info(
        "**Cara Penggunaan:**\n\n"
        "1. Isi data mahasiswa di form\n"
        "2. Klik **Prediksi Sekarang**\n"
        "3. Lihat hasil & rekomendasi intervensi"
    )
    st.divider()
    st.caption("Model: Random Forest | Accuracy: 87.91%")

# ─── Header ─────────────────────────────────────────────────────────────────────
st.title("🎓 Sistem Prediksi Dropout Mahasiswa")
st.markdown(
    "Masukkan data mahasiswa di bawah ini untuk memprediksi risiko **dropout** "
    "dan mendapatkan rekomendasi intervensi dini."
)
st.divider()

# ─── Input Form ─────────────────────────────────────────────────────────────────
with st.form("prediction_form"):

    # ── Program Studi ──────────────────────────────────────────────────────────
    st.subheader("📚 Informasi Program")
    col_prog1, col_prog2 = st.columns(2)
    with col_prog1:
        course_label = st.selectbox(
            "Program Studi",
            options=list(COURSE_OPTIONS.keys()),
            index=list(COURSE_OPTIONS.keys()).index('Nursing'),
        )
    with col_prog2:
        application_order = st.selectbox(
            "Pilihan Pendaftaran ke-",
            options=list(range(0, 10)),
            index=1,
            format_func=lambda x: f"Pilihan ke-{x}" if x > 0 else "Pilihan Pertama (0)",
            help="0 = pilihan pertama, 9 = pilihan terakhir"
        )

    st.divider()

    # ── Akademik ───────────────────────────────────────────────────────────────
    st.subheader("📋 Data Akademik")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Semester 1**")
        cu1_enrolled    = st.number_input("Jumlah Unit Diambil Sem-1",      0, 26, 6)
        cu1_approved    = st.number_input("Jumlah Unit Lulus Sem-1",        0, 26, 5,
                                          help="Berapa mata kuliah yang berhasil lulus")
        cu1_grade       = st.number_input("Nilai Rata-rata Sem-1 (0–20)",   0.0, 20.0, 12.0, step=0.1)
        cu1_evaluations = st.number_input("Jumlah Evaluasi Sem-1",          0, 45, 7)
        cu1_credited    = st.number_input("Unit Kredit Sem-1",              0, 20, 0)
        cu1_without_eval= st.number_input("Unit Tanpa Evaluasi Sem-1",      0, 12, 0)

    with col2:
        st.markdown("**Semester 2**")
        cu2_enrolled    = st.number_input("Jumlah Unit Diambil Sem-2",      0, 23, 6)
        cu2_approved    = st.number_input("Jumlah Unit Lulus Sem-2",        0, 23, 5,
                                          help="Berapa mata kuliah yang berhasil lulus")
        cu2_grade       = st.number_input("Nilai Rata-rata Sem-2 (0–20)",   0.0, 20.0, 12.0, step=0.1)
        cu2_evaluations = st.number_input("Jumlah Evaluasi Sem-2",          0, 33, 7)
        cu2_credited    = st.number_input("Unit Kredit Sem-2",              0, 19, 0)
        cu2_without_eval= st.number_input("Unit Tanpa Evaluasi Sem-2",      0, 12, 0)

    col_grade1, col_grade2 = st.columns(2)
    with col_grade1:
        admission_grade   = st.number_input("Nilai Masuk (0–200)",                   0.0, 200.0, 130.0, step=0.1)
    with col_grade2:
        prev_qual_grade   = st.number_input("Nilai Kualifikasi Sebelumnya (0–200)",  0.0, 200.0, 130.0, step=0.1)

    st.divider()

    # ── Demografis & Finansial ─────────────────────────────────────────────────
    st.subheader("👤 Data Demografis & Finansial")

    col3, col4, col5 = st.columns(3)
    with col3:
        gender_label      = st.radio("Jenis Kelamin",
                                     options=list(GENDER_OPTIONS.keys()),
                                     horizontal=True)
        scholarship_label = st.radio("Penerima Beasiswa",
                                     options=list(SCHOLARSHIP_OPTIONS.keys()),
                                     horizontal=True)
        tuition_label     = st.radio("Pembayaran SPP",
                                     options=list(TUITION_OPTIONS.keys()),
                                     horizontal=True,
                                     help="'Up to Date' = tepat waktu, 'In Arrears' = menunggak")

    with col4:
        debtor_label      = st.radio("Memiliki Hutang ke Institusi",
                                     options=list(YES_NO.keys()),
                                     horizontal=True)
        displaced_label   = st.radio("Mahasiswa Pindahan/Domisili",
                                     options=list(YES_NO.keys()),
                                     horizontal=True)
        international_label = st.radio("Mahasiswa Internasional",
                                       options=list(YES_NO.keys()),
                                       horizontal=True)

    with col5:
        special_needs_label = st.radio("Berkebutuhan Pendidikan Khusus",
                                       options=list(YES_NO.keys()),
                                       horizontal=True)
        age               = st.number_input("Usia Saat Mendaftar (tahun)", 17, 70, 20)
        marital_status    = st.selectbox("Status Pernikahan",
                                         options=[1, 2, 3, 4, 5, 6],
                                         format_func=lambda x: {
                                             1: "Lajang", 2: "Menikah",
                                             3: "Janda/Duda", 4: "Cerai",
                                             5: "Kumpul Kebo", 6: "Cerai Resmi"
                                         }[x])

    st.divider()

    # ── Latar Belakang Keluarga & Akademik Sebelumnya ─────────────────────────
    st.subheader("🏫 Latar Belakang")

    col6, col7 = st.columns(2)
    with col6:
        application_mode = st.selectbox(
            "Mode Pendaftaran",
            options=[1, 17, 18, 39, 42, 43, 2, 5, 7, 10, 15],
            format_func=lambda x: {
                1:  "Fase 1 – Umum",
                17: "Fase 2 – Umum",
                18: "Fase 3 – Umum",
                39: "Di atas 23 Tahun",
                42: "Transfer",
                43: "Ganti Program",
                2:  "Ordonansi No. 612/93",
                5:  "Kontingen Khusus (Azores)",
                7:  "Pemilik Gelar Lain",
                10: "Ordonansi No. 854-B/99",
                15: "Mahasiswa Internasional",
            }[x]
        )
        prev_qualification = st.selectbox(
            "Kualifikasi Pendidikan Sebelumnya",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: {
                1: "SMA / Sederajat",
                2: "Sarjana (S1)",
                3: "Diploma",
                4: "Magister (S2)",
                5: "Doktor (S3)",
                6: "Pernah Kuliah (tidak tamat)",
            }[x]
        )
        attendance = st.radio("Waktu Perkuliahan",
                              options=['Daytime', 'Evening'],
                              horizontal=True)

    with col7:
        nationality    = st.selectbox("Kewarganegaraan",
                                      options=[1, 41, 6, 103, 105, 22, 25, 2],
                                      format_func=lambda x: {
                                          1: "Portugal", 41: "Brazil",
                                          6: "Spanyol", 103: "Ukraina",
                                          105: "Rusia", 22: "Cape Verde",
                                          25: "Mozambik", 2: "Jerman"
                                      }.get(x, str(x)))
        mothers_qual   = st.number_input("Kualifikasi Pendidikan Ibu (kode)", 1, 44, 19)
        fathers_qual   = st.number_input("Kualifikasi Pendidikan Ayah (kode)", 1, 44, 12)
        mothers_occ    = st.number_input("Pekerjaan Ibu (kode)", 0, 194, 5)
        fathers_occ    = st.number_input("Pekerjaan Ayah (kode)", 0, 194, 9)

    st.divider()

    # ── Faktor Ekonomi Makro ───────────────────────────────────────────────────
    st.subheader("🌍 Kondisi Ekonomi")

    col8, col9, col10 = st.columns(3)
    with col8:
        unemployment_rate = st.slider("Tingkat Pengangguran (%)", 7.0, 17.0, 10.8, 0.1)
    with col9:
        inflation_rate    = st.slider("Tingkat Inflasi (%)", -0.8, 3.7, 1.4, 0.1)
    with col10:
        gdp               = st.slider("GDP", -4.1, 3.5, 1.74, 0.01)

    # ── Submit ─────────────────────────────────────────────────────────────────
    submitted = st.form_submit_button(
        "🔍 Prediksi Sekarang",
        use_container_width=True,
        type="primary"
    )

# ─── Prediction ─────────────────────────────────────────────────────────────────
if submitted:
    # Konversi label teks → kode numerik
    input_data = {
        'Marital_status':                               marital_status,
        'Application_mode':                             application_mode,
        'Application_order':                            application_order,
        'Course':                                       COURSE_OPTIONS[course_label],
        'Daytime_evening_attendance':                   1 if attendance == 'Daytime' else 0,
        'Previous_qualification':                       prev_qualification,
        'Previous_qualification_grade':                 prev_qual_grade,
        'Nacionality':                                  nationality,
        'Mothers_qualification':                        mothers_qual,
        'Fathers_qualification':                        fathers_qual,
        'Mothers_occupation':                           mothers_occ,
        'Fathers_occupation':                           fathers_occ,
        'Admission_grade':                              admission_grade,
        'Displaced':                                    YES_NO[displaced_label],
        'Educational_special_needs':                    YES_NO[special_needs_label],
        'Debtor':                                       YES_NO[debtor_label],
        'Tuition_fees_up_to_date':                      TUITION_OPTIONS[tuition_label],
        'Gender':                                       GENDER_OPTIONS[gender_label],
        'Scholarship_holder':                           SCHOLARSHIP_OPTIONS[scholarship_label],
        'Age_at_enrollment':                            age,
        'International':                                YES_NO[international_label],
        'Curricular_units_1st_sem_credited':            cu1_credited,
        'Curricular_units_1st_sem_enrolled':            cu1_enrolled,
        'Curricular_units_1st_sem_evaluations':         cu1_evaluations,
        'Curricular_units_1st_sem_approved':            cu1_approved,
        'Curricular_units_1st_sem_grade':               cu1_grade,
        'Curricular_units_1st_sem_without_evaluations': cu1_without_eval,
        'Curricular_units_2nd_sem_credited':            cu2_credited,
        'Curricular_units_2nd_sem_enrolled':            cu2_enrolled,
        'Curricular_units_2nd_sem_evaluations':         cu2_evaluations,
        'Curricular_units_2nd_sem_approved':            cu2_approved,
        'Curricular_units_2nd_sem_grade':               cu2_grade,
        'Curricular_units_2nd_sem_without_evaluations': cu2_without_eval,
        'Unemployment_rate':                            unemployment_rate,
        'Inflation_rate':                               inflation_rate,
        'GDP':                                          gdp,
    }

    input_df     = pd.DataFrame([input_data])[feature_names]
    input_scaled = scaler.transform(input_df)
    prediction   = model.predict(input_scaled)[0]
    probability  = model.predict_proba(input_scaled)[0]
    dropout_prob = probability[1]

    # ─── Hasil ────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Hasil Prediksi")

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        if prediction == 1:
            st.error("### ⚠️ BERISIKO DROPOUT")
        else:
            st.success("### ✅ TIDAK BERISIKO DROPOUT")
    with col_r2:
        st.metric("Probabilitas Dropout",
                  f"{dropout_prob*100:.1f}%",
                  delta="Tinggi" if dropout_prob > 0.5 else "Rendah")
    with col_r3:
        st.metric("Probabilitas Lulus / Melanjutkan",
                  f"{probability[0]*100:.1f}%")

    # Risk bar
    risk_pct = int(dropout_prob * 100)
    if dropout_prob < 0.33:
        color, risk_label = "green", "RENDAH"
    elif dropout_prob < 0.66:
        color, risk_label = "orange", "SEDANG"
    else:
        color, risk_label = "red", "TINGGI"

    st.markdown(f"""
**Tingkat Risiko: {risk_label}**
<div style="background:#e0e0e0; border-radius:10px; height:26px; width:100%; margin-bottom:6px;">
  <div style="background:{color}; border-radius:10px; height:26px; width:{risk_pct}%;
              display:flex; align-items:center; justify-content:center;
              color:white; font-weight:bold; min-width:40px;">
    {risk_pct}%
  </div>
</div>
""", unsafe_allow_html=True)

    # ─── Ringkasan Input ──────────────────────────────────────────────────────
    with st.expander("📋 Ringkasan Data yang Diinput"):
        summary = {
            "Program Studi":          course_label,
            "Jenis Kelamin":          gender_label,
            "Penerima Beasiswa":      scholarship_label,
            "Status Pembayaran SPP":  tuition_label,
            "Memiliki Hutang":        debtor_label,
            "Nilai Rata-rata Sem-1":  f"{cu1_grade:.1f}",
            "Nilai Rata-rata Sem-2":  f"{cu2_grade:.1f}",
            "Unit Lulus Sem-1":       cu1_approved,
            "Unit Lulus Sem-2":       cu2_approved,
            "Usia Pendaftaran":       age,
            "Nilai Masuk":            f"{admission_grade:.1f}",
        }
        st.table(pd.DataFrame(summary.items(), columns=["Atribut", "Nilai"]))

    # ─── Rekomendasi ──────────────────────────────────────────────────────────
    st.divider()
    st.subheader("💡 Rekomendasi Intervensi")

    if prediction == 1:
        recs = []
        if cu1_approved < 3 or cu2_approved < 3:
            recs.append(("📚 Bimbingan Akademik Intensif",
                         "Jadwalkan sesi konseling dan pendampingan dosen wali mingguan. "
                         "Mahasiswa hanya lulus sedikit unit kuliah — perlu perhatian ekstra."))
        if cu1_grade < 10 or cu2_grade < 10:
            recs.append(("📝 Program Remedial",
                         "Daftarkan ke kelas remedial atau kelompok belajar terpandu "
                         "untuk mendongkrak nilai semester berikutnya."))
        if tuition_label == 'In Arrears' or debtor_label == 'Yes':
            recs.append(("💰 Bantuan & Restrukturisasi Keuangan",
                         "Hubungkan dengan program beasiswa, keringanan SPP, "
                         "atau cicilan sebelum kondisi finansial memburuk lebih lanjut."))
        if scholarship_label == 'No':
            recs.append(("🏆 Ajuan Beasiswa",
                         "Dorong mahasiswa mendaftar program beasiswa institusi "
                         "atau beasiswa pemerintah yang tersedia."))
        if age > 25:
            recs.append(("🤝 Program Mahasiswa Nontraditional",
                         "Sediakan fleksibilitas jadwal (kelas malam/hybrid) dan "
                         "dukungan khusus untuk mahasiswa yang memiliki tanggung jawab lain."))
        if not recs:
            recs.append(("👨‍🏫 Monitoring Rutin",
                         "Lakukan pemantauan dan check-in bulanan bersama dosen wali "
                         "untuk memastikan mahasiswa tetap berada di jalur yang benar."))

        for title, desc in recs:
            st.warning(f"**{title}**\n\n{desc}")

    else:
        st.success(
            "✅ Mahasiswa ini memiliki risiko dropout yang **rendah**. "
            "Pertahankan performa dan dorong keterlibatan aktif dalam kegiatan akademik."
        )
        if cu1_grade > 15 and cu2_grade > 15:
            st.info(
                "🌟 **Potensi Berprestasi**: Nilai sangat baik! "
                "Pertimbangkan untuk mendaftarkan ke program penelitian atau beasiswa prestasi."
            )
