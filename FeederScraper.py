# yang diperlukan :
# pip install beautifulsoup4
# pip install requests
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Awal Class FeederScraper
class FeederScraper:
    def __init__(self, url, header, payload):

        # url yang ingin di scraping hiyahiya
        self.url = url

        # Request Headers
        # custom_header, terdapat cookie dan juga user-agent dari browser
        # untuk web-scrapping private-feeder.ulm.ac.id cookienya harus dimasukkan di custom_header dan ada beberapa hal yang memang harus diinclude di header agar bisa masuk
        self.header = header

        # Form Data
        self.payload = payload

    def main(self):
        session = requests.Session()

        # get(url, headers -- berfungsi untuk menghindari deteksi bahwa kita lagi scrapping)
        result = session.post(self.url, headers=self.header,data=self.payload)

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
        table = soup.findChildren('table', {"class": "table table-striped table-condensed"})

        # This will get the first (and only) table. Your page may have more.
        my_table = table[0]

        # You can find children with multiple tags by passing a list of strings
        # rows = my_table.findChildren(['th', 'tr'])
        rows = my_table.findChildren(['tr'])

        # tes hasil pencarian
        # print(rows[2])
        # print(rows[2])
        # print("\n")

        # initiate csv
        file = open('extract.csv','w', newline='')
        writer = csv.writer(file,delimiter=',')
        writer.writerow(['No', 'NIM', 'Nama Mahasiswa', 'Periode Masuk',' Status Keluar', 'Tanggal Keluar', 'Periode Lulus/DO', 'Status Aktivitas Kuliah Mahasiswa Per Semester (AKM)'])

        # mencari link yang belum memiliki akm
        i = 0
        prodi_not_empty = 0
        table_data = []
        for row in rows:
            if i >= 2 and i <= 4:  # 0 dan 1 adalah header dari table
                # Select a href ke 3 yang beiriskan link yang belum memiliki akm
                links = row.findChildren(['a'])[2]
                if links.text != "0":
                    # url akm
                    # print(links.attrs['href'])
                    # print(links.text)

                    # membuka url akm
                    url_akm = links.attrs['href'];
                    result_akm = session.post(url_akm, headers=self.header)
                    # Lihat hasil
                    # print(result_akm.text)
                    src_akm = result_akm.content
                    soup_akm = BeautifulSoup(src_akm, features="html.parser")
                    table_akm = soup_akm.findChildren('table', {"class": "content"})
                    my_table_akm = table_akm[0]
                    rows_akm = my_table_akm.findChildren(['tr'])
                    # lihat row akm
                    # print(rows_akm)

                    # # Method SO
                    # # Mengolah data agar disave ke excel
                    # tableMatrix = []
                    # # Here you can do whatever you want with the data! You can findAll table row headers, etc...
                    # list_of_rows = []
                    # jumlah_row = 0
                    # row_start = 0
                    # for row in my_table_akm.findAll('tr')[1:]:
                    #     if row_start >= 1 :
                    #         list_of_cells = []
                    #         for cell in row.findAll('td'):
                    #             text = cell.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('         ','')
                    #             list_of_cells.append(text)
                    #         list_of_rows.append(list_of_cells)
                    #         jumlah_row += 1
                    #     row_start += 1
                    # tableMatrix.append((list_of_rows, list_of_cells))
                    # # print(tableMatrix)
                    # # print(type(tableMatrix))
                    # # print(jumlah_row)

                    # METODE AZMI
                    # mengambil semua column dari masing-masing row
                    r = 0
                    for row_akm in rows_akm:
                        if r >= 2:
                            columns_akm = row_akm.findChildren(['td'])
                            # mengambil satu column dari semua column
                            row_data = []
                            for column_akm in columns_akm:
                                # print(column_akm.text.replace('			', '').replace(' 		', ''))
                                # print(column_akm.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('         ',''))
                                # filewriter.writerow([column_akm.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('         ','')])
                                if column_akm.text=='' :
                                    row_data.append(' ')
                                else :
                                    row_data.append(column_akm.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('         ',''))
                            writer.writerow(row_data)

                            # each individual row_data
                            # print(row_data)

                            table_data.append(row_data)
                        r += 1
                    prodi_not_empty += 1
            i += 1

        # semua data
        # print(table_data)

        # close file excel
        file.close()

        # jumlah data yang tidak kosong
        # print(prodi_not_em pty)

# Akhir Class FeederScraper
url = 'http://private-feeder.ulm.ac.id/'
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'Cookie':'PHPSESSID=imp9cfrlg69ko528blhkan3r14',
         'Connection':'keep-alive',
         'Cache-Control' : 'max-age=0',
         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
         'Host':'private-feeder.ulm.ac.id',
         'Accept-Encoding':'gzip, deflate'
         }
payload = {'jenis_chart': 'jumlahmhsnonakm',
           'id_smt': '20182'}

d = FeederScraper(url, header, payload)
d.main()







