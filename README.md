# 📄 Peningkatan Kualitas Citra Dokumen (Document Image Enhancement) - Tukang Scan

**Tugas Besar Pengolahan Citra Digital (PCD) - Institut Teknologi Sumatera (ITERA) 2025**

> **Kelompok 11 - Tukang Scan:**
> Fokus utama proyek ini adalah membangun *pipeline* otomatis untuk meningkatkan kualitas citra dokumen digital yang mengalami degradasi seperti *blur*, pencahayaan rendah (*low illumination*), dan bayangan (*shadow*) menggunakan kombinasi teknik pengolahan citra digital.

## 👥 Anggota Tim
| Nama | NIM | Peran |
| :--- | :--- | :--- |
| Andre Philip Tampubolon | 122140194 | Project Manager |
| Daniel Ferryal Zuhri | 122140144 | Image Processing Engineer |
| **Eric Arwido Damanik** | 122140157 | Data Analyst & Evaluator |
| Debora Sihombing | 122140032 | Research & Documentation Specialist |
| Alwi Arfan Solin | 122140197 | UI/UX Presentation Designer |

---

## 💡 Latar Belakang Proyek
Citra dokumen yang diambil menggunakan perangkat bergerak sering kali memiliki kualitas yang buruk karena faktor lingkungan seperti cahaya yang tidak merata atau guncangan. Proyek ini mengimplementasikan serangkaian algoritma untuk mengoreksi degradasi tersebut dan meningkatkan keterbacaan teks pada dokumen.

### Masalah Citra yang Ditangani (Dataset Sintetik):
1.  **Blur (Kekaburan):** Citra buram akibat fokus atau guncangan.
2.  **Low Illumination (Pencahayaan Rendah):** Citra yang terlalu gelap.
3.  **Shadow (Bayangan):** Citra yang tertutup bayangan (misalnya, dari ponsel atau tangan).

---

## 🛠️ Metodologi (Image Processing Pipeline)
Sistem ini memproses citra secara berurutan (*sequential pipeline*):

| Tahap | Metode | Tujuan |
| :--- | :--- | :--- |
| 1. Denoising | **Fast Non-Local Means Denoising** | Mengurangi *noise* dan artefak pada citra input. |
| 2. Contrast Enhancement | **CLAHE** (*Contrast Limited Adaptive Histogram Equalization*) | Meningkatkan kontras lokal dan meratakan distribusi pencahayaan, sangat efektif untuk kasus *Low Illumination*. |
| 3. Sharpening (Penajaman) | **Laplacian Operator + Canny Edge Masking** | Melakukan penajaman secara selektif. Penajaman hanya diterapkan pada area tepi (teks) yang terdeteksi oleh *Canny Edge Detector* untuk menghindari peningkatan *noise* di area latar belakang. |

---

## 📊 Hasil dan Evaluasi
Evaluasi dilakukan dengan membandingkan kualitas citra input dan citra hasil peningkatan (*output*) terhadap citra **Ground Truth (GT)** menggunakan metrik:
* **PSNR** (*Peak Signal-to-Noise Ratio*)
* **SSIM** (*Structural Similarity Index Measure*)

**Ringkasan Statistik (Setelah Program Dijalankan):**
Program akan menghasilkan `ringkasan_statistik.csv` yang berisi rata-rata perbaikan (ΔPSNR dan ΔSSIM) per kategori.

| Kategori | Perbaikan Utama | Peningkatan Metrik |
| :--- | :--- | :--- |
| **Low Illumination** | Peningkatan Kontras dan Kecerahan | PSNR & SSIM meningkat signifikan (Tertinggi). |
| **Shadow** | Perataan Pencahayaan | PSNR & SSIM meningkat (Sedang). |
| **Blur** | Penajaman Teks | SSIM umumnya meningkat, menunjukkan perbaikan visual. PSNR mungkin bervariasi karena sifat penajaman. |

---

Dosen Pengampu: Andika Setiawan, S.Kom., M.Cs.Dibuat oleh Kelompok 11 - Tukang Scan, FTI ITERA 2025.

---