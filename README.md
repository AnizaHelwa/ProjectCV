# ProjectCV
# Hand Gesture Recognition and Face Detection

Deskripsi:
Kode program ini merupakan gabungan dari beberapa fitur berbasis Computer Vision yang menggunakan OpenCV, MediaPipe, dan Pycaw. Program ini memungkinkan pengguna untuk:
1. Face Detection – Mendeteksi wajah secara real-time menggunakan model Haar Cascade.
2. Hand Tracking & Finger Counting – Mendeteksi tangan dan menghitung jumlah jari yang terbuka.
3. Volume Control dengan Gesture – Mengontrol volume sistem dengan gerakan jari (menggunakan jempol dan telunjuk).
4. Integrasi Face Detection dengan Hand Gesture – Mengombinasikan deteksi wajah dan kontrol berbasis gerakan tangan.

Fitur Utama:
A. Face Detection:
1. Menggunakan model Haar Cascade untuk mendeteksi wajah secara real-time dari video streaming kamera.
2. Menampilkan kotak di sekitar wajah yang terdeteksi.
   
B. Hand Gesture Recognition:
1. Mendeteksi tangan dan melacak posisi jari menggunakan MediaPipe.
2. Menghitung jumlah jari yang terbuka dan menampilkan hasilnya secara visual.
   
C. Volume Control dengan Gesture:
1. Menggunakan deteksi tangan untuk mengatur volume sistem berdasarkan jarak antara jempol dan telunjuk.
2. Volume berkurang jika jari didekatkan dan meningkat jika dijauhkan.
   
D. Penggabungan Face Detection dan Hand Gesture:
1. Program dapat mendeteksi wajah dan mengenali gerakan tangan dalam satu tampilan.

Teknologi yang Digunakan:
a. Python 3
b. OpenCV
c. MediaPipe
d. Pycaw (Python Core Audio Windows) – untuk mengontrol volume sistem
e. NumPy
f. Math (untuk perhitungan jarak antara jari)

Resource: 
1. https://youtu.be/01sAkU_NvOY?si=hKgLymp8DYleXlLp
2. https://youtu.be/51XVxq8Rhv4?si=VGa_A4hRabMF7lm8
3. https://youtu.be/oXlwWbU8l2o?si=UDOYqJ5hguluc9qx
