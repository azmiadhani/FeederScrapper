# YouTube Link:

# Let's obtain the links from the following website:
# https://forlap.ristekdikti.go.id/prodi/detail/ODlCN0VEOTEtRjAwRC00ODdGLUJEQjMtQTlFOTA5OEIyM0Ew/0

# Goal: Extract all of the links on the page that point to the
# briefings and statements.

import requests
from bs4 import BeautifulSoup

# cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
result = requests.get("https://forlap.ristekdikti.go.id/prodi/detail/ODlCN0VEOTEtRjAwRC00ODdGLUJEQjMtQTlFOTA5OEIyM0Ew/0", headers={'User-Agent': 'Mozilla/5.0'})

src = result.content

soup = BeautifulSoup(src, features="html.parser")

links = soup.find_all("article")
# print(links)

for link in links:
    # print(link.find('p', attrs={'class': 'briefing-statement__type'}))
    print(link.find('a').text)
    print(link.find('a').attrs['href'])
