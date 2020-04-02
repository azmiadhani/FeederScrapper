# yang diperlukan :
# pip install beautifulsoup4
# pip install requests
import requests
from bs4 import BeautifulSoup

# url yang ingin di scraping hiyahiya
url = 'https://www.socialblade.com/youtube/top/50/'

# get(url, headers -- berfungsi untuk menghindari deteksi bahwa kita lagi scrapping)
result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# untuk memastikan bahwa url accessible dengan keterangan
# 200 OK
# 401 Unauthorized
# 403 Forbidden
# 407 Proxy Auth Required
# maka :
# print(result.status_code)

# mendapatkan informasi header
# print(result.headers)

# menyimpan konten website
src = result.content
# print(src)

# objek BeautifulSoup
soup = BeautifulSoup(src, features="html.parser")

# mencari semua tag yang diinginkan
links = soup.find_all("a")
# tes hasil pencarian
# print(links)
# print("\n")

for link in links:
    if "Login" in link.text:
        print(link)
        print(link.attrs['href'])