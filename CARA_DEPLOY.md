# Panduan Deploy "Dapur Cilok" ke Vercel

Website ini dibuat menggunakan **Flask (Python)** dan sudah dikonfigurasi agar siap dideploy ke **Vercel** secara GRATIS.

## ⚠️ Catatan Penting
Karena Vercel menggunakan sistem *Serverless*, database SQLite (`dapur_cilok.db`) yang digunakan di proyek ini bersifat **Read-Only** atau akan **ter-reset** setiap kali ada deployment baru.
- Artinya: Data menu yang sudah ada akan tampil.
- Namun: Jika Anda menambah/edit menu lewat Admin Dashboard di Vercel, perubahan itu **MUNGKIN HILANG** setelah beberapa saat.
- Solusi Jangka Panjang: Gunakan database eksternal seperti **Supabase** atau **PostgreSQL** jika ingin data tersimpan permanen.

---

## Langkah 1: Upload ke GitHub

1. Pastikan Anda sudah login ke [GitHub](https://github.com).
2. Buat repository baru (klik tombol **+** di pojok kanan atas -> **New repository**).
3. Beri nama, misalnya `dapur-cilok-web`.
4. Jangan centang "Add a README file" (biarkan kosong).
5. Di terminal komputer Anda (di folder proyek ini), jalankan perintah untuk push ke remote repository Anda.

---

## Langkah 2: Deploy di Vercel

1. Buka [Vercel Dashboard](https://vercel.com/dashboard) dan login (bisa pakai akun GitHub).
2. Klik tombol **"Add New..."** -> **"Project"**.
3. Di bagian **Import Git Repository**, cari repo `dapur-cilok-web` yang baru saja Anda buat, lalu klik **Import**.
4. Di halaman **Configure Project**:
   - **Framework Preset**: Biarkan "Other" atau pilih "Flask" jika ada (biasanya otomatis terdeteksi Python).
   - **Root Directory**: Biarkan `./`.
   - **Build Command**: Kosongkan (Vercel otomatis install dari `requirements.txt`).
   - **Output Directory**: Kosongkan.
   - **Environment Variables**: (Opsional, tidak perlu diisi sekarang).
5. Klik **Deploy**.

Tunggu sekitar 1-2 menit. Vercel akan membangun website Anda. Jika sukses, Anda akan melihat tampilan confetti 🎉 dan link website Anda (misal: `https://dapur-cilok-web.vercel.app`).

---

## Cara Login Admin
- **URL Admin**: `https://NAMA-APP-ANDA.vercel.app/admin`
- **Username**: `admin`
- **Password**: `password123`

Selamat! Warung seblak online Anda sudah jadi! 🌶️🔥
