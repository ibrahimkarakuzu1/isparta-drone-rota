#  Isparta AFAD Drone Lojistik Hattı - Rota Optimizasyonu

Bu proje, **Yapay Zeka Sınavı Proje-2 (Senaryo 8)** kapsamında geliştirilmiştir. Olası bir afet durumunda, Isparta il merkezi ve çevre dağ köylerindeki toplanma alanlarına acil ilaç/gıda taşıyan bir drone filosu için **en kısa ve en verimli rotayı** belirlemeyi amaçlar.

##  Projenin Amacı
Karayollarının kullanılamaz olduğu afet senaryolarında, 90'a yakın gerçek toplanma alanına ulaşmak için **Gezgin Satıcı Problemi'ni (TSP)** doğadan esinlenen **Karınca Kolonisi Algoritması (ACO - Ant Colony Optimization)** kullanarak çözmek.

##  Özellikler
* **Gerçek Veri Seti:** e-Devlet AFAD sisteminden alınan 90'a yakın gerçek koordinat (Enlem/Boylam).
* **Modüler Mimari:** `Core` (Algoritma), `Data` (Veri) ve `Main` (Arayüz) katmanlarına ayrılmış profesyonel yapı.
* **Haversine Formülü:** Drone uçuşu simüle edildiği için kuş uçuşu mesafe hesaplaması.
* **İnteraktif Arayüz:** Streamlit ile geliştirilmiş parametre kontrol paneli.
* **Görselleştirme:** Folium haritası üzerinde dinamik rota çizimi ve iterasyon grafikleri.

## 📂 Proje Yapısı
```text
yzs_proje2_drone/
├── core/                  # Algoritma ve Matematiksel İşlemler
│   ├── ant_algorithm.py   # Karınca Kolonisi Algoritması (ACO) Sınıfı
│   └── matrix_utils.py    # Mesafe Matrisi ve Haversine Hesaplamaları
├── data/                  # Veri Katmanı
│   └── coordinates.py     # Isparta AFAD Toplanma Alanları Veri Seti
├── main.py                # Streamlit Ana Uygulaması (Arayüz)
├── requirements.txt       # Gerekli Kütüphaneler
└── README.md              # Proje Dokümantasyonu
