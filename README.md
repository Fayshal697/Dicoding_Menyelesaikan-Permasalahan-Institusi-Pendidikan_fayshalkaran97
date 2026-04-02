# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang baik. Namun, tingginya angka mahasiswa yang tidak menyelesaikan pendidikan (dropout) menjadi permasalahan serius yang perlu segera ditangani. Dropout tidak hanya merugikan mahasiswa secara individu, tetapi juga berdampak pada reputasi dan akreditasi institusi.

### Permasalahan Bisnis

Permasalahan bisnis yang dihadapi Jaya Jaya Institut adalah sebagai berikut:

1. **Tingginya angka dropout**: Dari 4.424 mahasiswa dalam dataset, sebanyak 1.421 mahasiswa (32,1%) berstatus dropout — angka yang signifikan dan perlu ditekan.
2. **Deteksi dini yang lemah**: Institusi tidak memiliki sistem yang dapat mengidentifikasi mahasiswa berisiko dropout sejak dini, sehingga intervensi seringkali terlambat.
3. **Alokasi sumber daya yang tidak terarah**: Tanpa data prediktif, program bimbingan dan bantuan keuangan tidak dapat diarahkan secara efisien kepada mahasiswa yang paling membutuhkan.

### Cakupan Proyek

Cakupan proyek yang dikerjakan meliputi:

- **Eksplorasi dan Analisis Data (EDA)**: Memahami karakteristik data dan pola-pola yang berhubungan dengan status mahasiswa.
- **Preprocessing Data**: Membersihkan dan mempersiapkan data untuk pemodelan machine learning.
- **Pembangunan Model Machine Learning**: Membuat model klasifikasi untuk memprediksi risiko dropout.
- **Evaluasi Model**: Menilai performa model menggunakan berbagai metrik evaluasi.
- **Business Dashboard**: Membangun dashboard interaktif untuk monitoring dan pemahaman data.
- **Deployment Prototype**: Menyediakan aplikasi berbasis web yang dapat digunakan langsung oleh staf institusi.

### Persiapan

**Sumber data:**
 `https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv` 

**Setup environment:**

```bash
pip install -r requirements.txt
```

---

## Business Dashboard

Dashboard bisnis dibuat menggunakan **Metabase** (atau Tableau/Looker Studio) untuk memvisualisasikan data mahasiswa secara interaktif, mencakup:

- **Distribusi Status Mahasiswa** — proporsi Graduate, Dropout, dan Enrolled
- **Tren Dropout berdasarkan Program Studi** — program studi mana yang paling berisiko
- **Analisis Faktor Akademik** — perbandingan nilai dan unit lulus antara status mahasiswa
- **Profil Demografis** — distribusi gender, usia, beasiswa, dan status pembayaran SPP
- **Faktor Risiko Finansial** — proporsi mahasiswa yang memiliki tunggakan vs. pembayaran tepat waktu

> **Cara mengakses dashboard:**
> Jalankan Metabase secara lokal dengan Docker:
> ```bash
> docker run -d -p 3000:3000 --name metabase metabase/metabase:v0.46.4
> ```
> Kemudian buka `http://localhost:3000` di browser.

### Akses Dashboard Metabase

Email: fayshalathilla@mail.com  
Password: kamumahir3

---

## Menjalankan Sistem Machine Learning

Prototype sistem machine learning dibuat menggunakan **Streamlit** dan dapat dijalankan dengan langkah berikut:

```bash
# Jalankan aplikasi Streamlit secara lokal
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

**Cara menggunakan prototype:**
1. Isi data akademik mahasiswa (nilai, jumlah unit yang lulus, dll.)
2. Isi data demografis dan finansial (gender, beasiswa, status SPP, dll.)
3. Klik tombol **"Prediksi Sekarang"**
4. Lihat hasil prediksi risiko dropout beserta rekomendasi intervensi

> **Link Prototype (Streamlit Community Cloud):**
> 🔗 [https://jaya-jaya-dropout-prediction.streamlit.app](https://jaya-jaya-dropout-prediction.streamlit.app)
> *(Ganti link ini dengan URL deployment Anda setelah deploy ke Streamlit Cloud)*

**Cara deploy ke Streamlit Community Cloud:**
1. Upload semua file (`app.py`, `model.pkl`, `scaler.pkl`, `feature_names.pkl`, `data.csv`, `requirements.txt`) ke GitHub
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud) dan login
3. Klik **New App** → pilih repository dan file `app.py`
4. Klik **Deploy**

---

## Conclusion

Berdasarkan hasil proyek data science yang telah dikerjakan, diperoleh kesimpulan sebagai berikut:

### Temuan Utama

1. **Tingkat dropout sebesar 32,1%** (1.421 dari 4.424 mahasiswa) merupakan angka yang cukup mengkhawatirkan dan membutuhkan perhatian serius dari institusi.

2. **Faktor akademik semester 1 dan 2 adalah prediktor terkuat** dropout mahasiswa. Secara spesifik, jumlah unit mata kuliah yang berhasil lulus (`Curricular_units_2nd_sem_approved`) dan rata-rata nilai (`Curricular_units_2nd_sem_grade`) adalah dua fitur paling penting dalam prediksi.

3. **Faktor finansial sangat berpengaruh**: Mahasiswa yang menunggak pembayaran SPP (`Tuition_fees_up_to_date = 0`) dan yang memiliki hutang (`Debtor = 1`) memiliki kecenderungan dropout yang jauh lebih tinggi.

4. **Usia saat mendaftar** juga menjadi faktor risiko — mahasiswa yang mendaftar di usia lebih tua (di atas 25 tahun) cenderung lebih berisiko dropout, kemungkinan karena memiliki tanggung jawab lain di luar kuliah.

5. **Model Random Forest** berhasil memprediksi mahasiswa berisiko dropout dengan performa yang baik:
   - **Accuracy**: 87,91%
   - **Precision**: 84,98%
   - **Recall**: 75,70%
   - **F1-Score**: 80,07%

### Rekomendasi Action Items

Berdasarkan hasil analisis dan pemodelan, berikut rekomendasi action items yang dapat diikuti oleh Jaya Jaya Institut:

1. **Implementasikan sistem monitoring berbasis model ML** — Integrasikan prototype prediksi dropout ke dalam sistem akademik internal. Jalankan prediksi secara otomatis di akhir semester 1 untuk mengidentifikasi mahasiswa berisiko sebelum terlambat.

2. **Program bimbingan akademik intensif** — Prioritaskan mahasiswa yang memiliki nilai rata-rata di bawah 10 atau jumlah unit lulus kurang dari 3 pada semester pertama untuk mendapatkan sesi konseling dan pendampingan dosen wali secara terjadwal.

3. **Perkuat program bantuan keuangan** — Buat mekanisme deteksi dini untuk mahasiswa yang mulai menunggak SPP dan hubungkan langsung dengan program beasiswa, keringanan, atau cicilan sebelum kondisi memburuk.

4. **Evaluasi program studi dengan dropout tertinggi** — Identifikasi program studi yang memiliki angka dropout di atas rata-rata dan lakukan kajian kurikulum, beban studi, serta kualitas pengajaran di program tersebut.

5. **Program khusus untuk mahasiswa nontraditional** — Sediakan skema kuliah yang lebih fleksibel (kelas malam, hybrid, atau part-time) untuk mahasiswa berusia di atas 25 tahun yang umumnya memiliki tanggung jawab lain di luar akademik.

6. **Dashboard monitoring real-time** — Gunakan business dashboard yang telah dibuat untuk memantau KPI dropout secara berkala (bulanan/semesteran) agar manajemen institusi dapat mengambil keputusan berbasis data secara cepat.
