Web : https://akhtar-eijaz-futbolarchive.pbp.cs.ui.ac.id/

Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

Membuat sebuah proyek Django baru : Membuat direktori baru untuk Football Shop, untuk Football Shop saya menamakan dengan nama futbol-archive, lalu masuk ke dalam direktori tersebut lalu buka terminal, buat virtual environment dengan menjalankan perintah python -m venv env, mengaktifkan virtual environment dengan perintah env\Scripts\activate, buat berkas requirements.txt yang isinya adalah dependencies di direktori Football Shop yang telah dibuat, install dependencies dengan cara menjalankan perintah pip install -r requirements.txt, buat proyek Django dengan perintah django-admin startproject futbol_archive .



Membuat aplikasi dengan nama main pada proyek tersebut : Jalankan perintah python manage.py startapp main pada terminal direktori futbol-archive, mendaftarkan aplikasi main ke dalam proyek dengan cara menambahkan 'main' ke elemen terakhir dari INSTALLED_APPS yang berada di settings.py



Melakukan routing pada proyek agar dapat menjalankan aplikasi main, Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu, Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py : Membuat direktori templates di dalam direktori aplikasi main dan membuat main.html di dalam direktori templates, isi main.html dengan

<h1>Futbol Archive</h1>

<h5>Name: </h5>
<p>{{ name }}<p>
<h5>Class: </h5>
<p>{{ class }}</p>

Buka views.py dan diisi dengan

from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Akhtar Eijaz Putranto',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)

Buat urls.py di direktori main dan diisi dengan

from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]

Buka urls.py di direktori futbol_archive dan tambahkan "path('', include('main.urls'))" di dalam list urlpatterns



Membuat model pada aplikasi main dengan nama Product : Buka berkas models.py pada direktori aplikasi main, isi berkas tersebut dengan

from django.db import models

class Product(models.Model):
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField()
    is_featured = models.BooleanField()

Dengan ini sudah terbuat model Product dengan atribut name, price, description, thumbnail, category, dan is_featured



Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet : Buka terminal di direktori futbol-archive dan jalankan perintah berikut

git remote add pws https://pbp.cs.ui.ac.id/akhtar.eijaz/futbolarchive
git branch -M master
git push pws master

Setelah itu jika status build sudah running, maka website https://akhtar-eijaz-futbolarchive.pbp.cs.ui.ac.id/ sudah bisa diakses



Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html :

![Bagan Client Request Django](image.png)

Fungsi urls.py adalah untuk mencocokkan path request ke view tertentu dan menghubungkan URL dari fungsi di views.py. Fungsi views.py adalah untuk menyusun context dan merender template html dan mengambil data dari models.py. Fungsi models.py adalah untuk mendefinisikan tabel yang akan menjadi model data dan menyediakan data ke views.py yang akan dikirimkan ke template html. Fungsi berkas html adalah untuk menampilkan context yang diambil dari views.py kepada user.



Jelaskan peran settings.py dalam proyek Django : settings.py dalam proyek Django adalah file konfigurasi utama di Django yang mengatur database, aplikasi, keamanan, dan bahasa. Bagian-bagian settings.py yang dimodifikasi pada Tugas 2 ini diantara lain :
1. ALLOWED_HOSTS : Ini adalah bagian settings.py berbentuk list yang isinya adalah domain yang bisa mengakses server Django. Disini saya menambahkan "localhost", "127.0.0.1", dan url deployment tugas
2. INSTALLED_APPS : Ini adalah bagian settings.py berbentuk list yang isinya adalah daftar aplikasi yang digunakan. Disini saya menambahkan aplikasi yang dibuat yaitu 'main'
3. DATABASE : Ini adalah bagian settings.py yang mengatur database project. Disini saya menambahkan database yang diberikan, seperti name, user, host, port, password



Bagaimana cara kerja migrasi database di Django : Pertama-tama harus membuat file migrasi terlebih dahulu dengan cara menjalankan perintah python manage.py makemigrations di direktori proyek Django fungsinya adalah untuk membaca semua perubahan yang diubah di models.py lalu jalankan python manage.py migrate fungsinya adalah Django membaca semua file migrasi yang belum dijalankan dan menerapkan skema model yang telah dibuat ke dalam database Django lokal



Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak : Mungkin salah satunya karena Django menggunakan bahasa Python yang dikenal mudah dan sintaksnya mudah dipahami dan Django digunakan oleh beberapa perusahaan besar juga, seperti Instagram, Spotify, YouTube



Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya : Tidak, tutorial 1 sudah cukup jelas dan mudah dimengerti