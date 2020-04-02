# YouTube Link:

# Let's obtain the links from the following website:
# https://www.whitehouse.gov/briefings-statements/

# One of the things this website consists of is records of presidential
# briefings and statements.

# Goal: Extract all of the links on the page that point to the
# briefings and statements.

import requests
from bs4 import BeautifulSoup

# cookies yang diperlukan
cookies = {'SimpleSAMLSimari': '085f0b94ebe675f7dbd5e5eceb3ab24e','simari_session':'a9qpjuhml4ouc1r4r3vqduo74tdaufpc'}

# url
# cookies <- dari variabel cookies
# headers <- ada beberapa website yang mendeteksi user itu asli atau scraper
result = requests.get("https://portal.ulm.ac.id/profil/mahasiswa", cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'})

# untuk memastikan bahwa url accessible dengan keterangan
# 200 OK
# 401 Unauthorized
# 403 Forbidden
# 407 Proxy Auth Required
# maka :
# print(result.status_code)
# exit()

src = result.content

soup = BeautifulSoup(src, features="html.parser")

links = soup.find_all("h3")
# print(links)

for link in links:
    # print(link.find('p', attrs={'class': 'briefing-statement__type'}))
    # print(link.find('h3'))
    # print(link.find('h3').attrs['href'])
    print(link.text)
