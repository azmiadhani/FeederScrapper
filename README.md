# Feeder Scrapper

[![Python 3.8.2](https://img.shields.io/badge/python-3.8.2-blue.svg)](https://www.python.org/downloads/release/python-382/)

Web Scrapper for feeder

## Screenshot
![Screenshot](https://github.com/azmiadhani/FeederScrapper/blob/master/screenshot/1.png)
![Screenshot](https://github.com/azmiadhani/FeederScrapper/blob/master/screenshot/2.png)


## Getting Started

Download file melalui repo ini, ekstrak file yang telah didownload, masuk kedalam direktori utama yang berisikan file .py.
Aplikasi ini di-development menggunakan python 3.8.2

### Prerequisites

Ada beberapa requirement yang harus diinstal sebelum aplikasi bisa dijalankan. Cara menginstallnya pertama-tama buka cmd dan arahkan cmd ke direktori utama yang berisikan file.py, setelah itu jalankan command ini : 

```
pip install -r requirements.txt
```

Tunggu hingga selesai penginstallan requirements yang diperlukan.

### Installing

Setelah requirement telah diinstal maka selanjutnya kita akan menjalankan aplikasi. Dengan cmd berada pada direktori utama dari aplikasi maka selanjutnya jalankan command ini untuk menjalankan aplikasi

```
python FeederScrapper.py
```

Untuk default launch-nya bisa menggunakan command diatas, namun cookies expiring mungkin terjadi sehingga kita perlu memasukkan cookie yang baru kedalam command launch aplikasi agar bisa mengakses data yang diperlukan, untuk command-command-nya bisa dilihat dengan cara memasukkan command ini : 

```
python FeederScrapper.py --cookie COOKIEVALUE --semester SEMESTERVALUE --report ON/OFF
```


## Authors

* **Azmi Adhani**

Lihat juga [contributors](https://github.com/azmiadhani/FeederScrapper/contributors) yang berpartisipasi di project ini.
