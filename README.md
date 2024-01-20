# PT SAS Kreasindo - Technical Test

- Versi Odoo : 15
- Environment : Docker
- Public Running Port : 8000 (Odoo)
- Public Running Port : 5430 (PostgreSQL)
- Nama Modul : Custom Angganix (custom_angganix)

Untuk dapat menjalankan project, dapat melakukan installasi docker-desktop agar lebih mudah. lalu pergi ke root directory project, type command

`$ docker-compose up -d
`

lalu buka browser dan akses odoo di port **8000** -> **http://localhost:8000**
setup odoo seperti biasa. 

***Catatan (untuk dapat membuka akses import SO Line)***

 1. Aktifkan terlebih dahulu mode developer
 2. Pergi ke **Setting** -> **Technical** -> **Security** -> **Access Right**
 3. Tambahkan Access Control Baru  **(New)**
 4. Isi kolom Nama dengan **"Import Sale Order Lines Wizard"**
 5. Isi Kolom Model dengan **"Import Sale Order Lines Wizard"**
 6. Isi Kolom User dengan **"User / Type Internal"**
 7. Checklist semua akses
 8. Save

Sekian informasi dari project technical test yang saya kerjakan, jika ada kekurangan saya mohon maaf sebesar-besarnya. 
#
Terima Kasih

***Angga NIX***

