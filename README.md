# Dashboard Data Pasar — Django

Versi ini dibuat ulang agar bisa berjalan lokal tanpa Supabase. Jika `DATABASE_URL` tersedia, Django otomatis memakai PostgreSQL.

## 1. Instalasi Windows

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buka `http://127.0.0.1:8000/login/`.

## 2. Format file Excel

Nama file:

- `100 A 2020-2025.xlsx`
- `100 L 2020-2025.xlsx`
- `100 T 2020-2025.xlsx`

Pemetaan:
- 100 = Selatan
- 200 = Timur
- 300 = Utara
- A = Air
- L = Listrik
- T = Tempat

Kolom Excel dikenali secara fleksibel untuk:
Tgl Bayar, Tgl Closing, Pasar, Nama Pasar, Alamat, Stand, Pedagang, Periode, Nilai, Kode Cabang, Cabang, Jenis Tagihan.

## 3. Validasi

Sebelum dijalankan:

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
```

## 4. Deploy Render

Isi `DATABASE_URL` dengan connection string PostgreSQL. Jangan commit `.env` atau password database ke Git.
