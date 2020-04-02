# yang diperlukan :
# pip install beautifulsoup4
# pip install requests
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# url yang ingin di scraping hiyahiya
url = 'http://private-feeder.ulm.ac.id/'

# Request Headers
# custom_header, terdapat cookie dan juga user-agent dari browser
# untuk web-scrapping private-feeder.ulm.ac.id cookienya harus dimasukkan di custom_header dan ada beberapa hal yang memang harus diinclude di header agar bisa masuk
custom_header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                 'Cookie':'PHPSESSID=imp9cfrlg69ko528blhkan3r14',
                 'Connection':'keep-alive',
                 'Cache-Control' : 'max-age=0',
                 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                 'Host':'private-feeder.ulm.ac.id',
                 'Accept-Encoding':'gzip, deflate'
                 }

# Form Data
payload = {'jenis_chart':'jumlahmhsnonakm',
           'id_smt':'20182'}


# get(url, headers -- berfungsi untuk menghindari deteksi bahwa kita lagi scrapping)
session = requests.Session()
result = session.post(url, headers=custom_header,data=payload)

# untuk memastikan bahwa url accessible dengan keterangan
# 200 OK
# 401 Unauthorized
# 403 Forbidden
# 407 Proxy Auth Required
# maka :
# print(result.status_code)
# print(result.headers)
# print(result.text)
# exit()

# mendapatkan informasi header
# print(result.headers)

# menyimpan konten website
src = result.content
# print(src)
# exit()

# objek BeautifulSoup
soup = BeautifulSoup(src, features="html.parser")

# mencari semua tag yang diinginkan
# links = soup.find_all("img")
table = soup.findChildren('table', {"class":"table table-striped table-condensed"})

# This will get the first (and only) table. Your page may have more.
my_table = table[0]

# You can find children with multiple tags by passing a list of strings
# rows = my_table.findChildren(['th', 'tr'])
rows = my_table.findChildren(['tr'])

# tes hasil pencarian
# print(rows[2])
# print(rows[2])
# print("\n")

# mencari link yang belum memiliki akm
i=0
prodi_not_empty = 0
all_data = []
for row in rows :
    if i == 2 : # 0 dan 1 adalah header dari table
        # Select a href ke 3 yang beiriskan link yang belum memiliki akm
        links = row.findChildren(['a'])[2]
        if links.text != "0" :
            # url akm
            # print(links.attrs['href'])
            # print(links.text)

            # membuka url akm
            url_akm = links.attrs['href'];
            result_akm = session.post(url_akm, headers=custom_header)
            # Lihat hasil
            # print(result_akm.text)
            src_akm = result_akm.content
            soup_akm = BeautifulSoup(src_akm, features="html.parser")
            table_akm = soup_akm.findChildren('table', {"class": "content"})
            my_table_akm = table_akm[0]
            rows_akm = my_table_akm.findChildren(['tr'])
            # lihat row akm
            # print(rows_akm)

            # mengambil semua column dari masing-masing row
            r=0
            for row_akm in rows_akm:
                row_data = []
                if r >= 2:
                    columns_akm = row_akm.findChildren(['td'])
                    # mengambil satu column dari semua column
                    for column_akm in columns_akm:
                        print(columns_akm)
                        
                r += 1

            prodi_not_empty += 1
    i += 1

# jumlah data yang tidak kosong
# print(prodi_not_empty)