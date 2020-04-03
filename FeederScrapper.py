# yang diperlukan :
# pip install beautifulsoup4
# pip install requests
# pip install requests
# pip install tqdm
#pip install argparse

# untuk excel
import csv
# untuk cprint
import sys
from termcolor import colored, cprint
# untuk requests
import requests
# untuk beautifulsoup
from bs4 import BeautifulSoup
from tqdm import tqdm
# python argument
import argparse
# untuk waktu
from datetime import date
from datetime import datetime

# Awal Class FeederScraper
class FeederScraper:
    def __init__(self, url, header, payload, report):

        # url yang ingin di scraping hiyahiya
        self.url = url

        # Request Headers
        # custom_header, terdapat cookie dan juga user-agent dari browser
        # untuk web-scrapping private-feeder.ulm.ac.id cookienya harus dimasukkan di custom_header dan ada beberapa hal yang memang harus diinclude di header agar bisa masuk
        self.header = header

        # Form Data
        self.payload = payload

        # report
        self.report = report

    def main(self):
        session = requests.Session()

        # get(url, headers -- berfungsi untuk menghindari deteksi bahwa kita lagi scrapping)
        try :
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
            # print(rows)
            # print(rows[2])
            # exit()

            # initiate csv
            nama_file = 'extract.csv'
            file = open(nama_file,'w', newline='')
            writer = csv.writer(file,delimiter=',')
            writer.writerow(['No', 'NIM', 'Nama Mahasiswa', 'Periode Masuk',' Status Keluar', 'Tanggal Keluar', 'Periode Lulus/DO', 'Status Aktivitas Kuliah Mahasiswa Per Semester (AKM)'])

            # mencari link yang belum memiliki akm
            i = 0
            prodi_not_empty = 0
            table_data = []
            jumlah_data = 0
            report=[]
            report_error=[]
            for row in tqdm(rows):
                # if i == 44 : # 0 dan 1 adalah header dari table
                if i == 2 : # 0 dan 1 adalah header dari table

                    jumlah_baris = 0

                    # Output Nama Prodi
                    # Select a href ke 3 yang beiriskan link yang belum memiliki akm
                    links = row.findChildren(['a'])[2]
                    # url akm
                    # print(links.attrs['href'])
                    # print(links.text)

                    # membuka url akm
                    url_akm = links.attrs['href'];
                    result_akm = session.post(url_akm, headers=self.header)
                    if result_akm.status_code != 200 :
                        report_error.append('Error ' + str(result_akm.status_code) + ' - ' + links.attrs['href']);
                    else :
                        # Lihat hasil
                        # print(result_akm.text)
                        src_akm = result_akm.content
                        soup_akm = BeautifulSoup(src_akm, features="html.parser")
                        table_akm = soup_akm.findChildren('table', {"class": "content"})
                        my_table_akm = table_akm[0]
                        rows_akm = my_table_akm.findChildren(['tr'])
                        # lihat row akm
                        # print(rows_akm)

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

                                jumlah_baris += 1
                            r += 1
                        prodi_not_empty += 1
                        jumlah_data=jumlah_baris+jumlah_data
                        if jumlah_baris == 0 :
                            color = 'red'
                        else :
                            color = 'blue'
                        report_row = []
                        report_row.append(row.findChildren(['td'])[1].text)
                        report_row.append("Jumlah Baris : " + str(jumlah_baris))
                        report.append(report_row)
                        # cprint(row.findChildren(['td'])[1].text,'white')
                        # cprint("Jumlah Baris : " + str(jumlah_baris) + '\n', color)
                i += 1
            # print(report)

            file.close()

            # reporting
            if self.report=="on":
                print('\n')
                for rep in report:
                    print(rep[0])
                    print(rep[1])

            # Error Reporting to error.txt
            f = open("error.txt", "w+")
            jumlah_error = 0
            for re in report_error:
                f.write(re +" \r\n")
                jumlah_error+=1
            f.close()

            # Summary
            print('\n')
            print('[' + datetime.now().strftime("%H:%M:%S") + ']',end='')
            print(' [REPORT]  ', end='')
            print('Jumlah Error : ' + str(jumlah_error) + ' (untuk detail bisa dilihat di-file error.txt)')
            print('[' + datetime.now().strftime("%H:%M:%S") + ']',end='')
            print(' [INFO]  ', end='')
            print('File csv telah disimpan dengan nama : ' + nama_file)
            print('[' + datetime.now().strftime("%H:%M:%S") + ']',end='')
            print(' [SELESAI]  ',end='')
            print('Total Baris : '+str(jumlah_data))

            # semua data
            # print(table_data)

            # close file excel

            # jumlah data yang tidak kosong
            # print(prodi_not_em pty)
        except session.exceptions.HTTPError as err:
            pass

# Akhir Class FeederScraper

# dieksekusi saat .py dibuka :
url = 'http://private-feeder.ulm.ac.id/'
print('Private Feeder Scrapper')
print('Versi 1.0.0')
print('\n')
print('[*] dimulai @ '+date.today().strftime("/%d-%m-%Y/") + ' ' + datetime.now().strftime("%H:%M:%S"))
print('\n')


parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--cookie", default='imp9cfrlg69ko528blhkan3r14', help="ini adalah cookie dari aplikasi feeder (PHPSESSID) dengan format : 'COOKIEVALUE' (menggunakan petik)")
parser.add_argument("--semester", default='20182', help="ini adalah form_data dari aplikasi feeder saat berada dihalaman 'http://private-feeder.ulm.ac.id/home', form_data bisa dilihat melalui Inspect Element, semester dengan contoh format : '20182' (menggunakan petik)")
parser.add_argument("--report", default='on', help="ini adalah option untuk menampilkan report jumlah baris per-prodi, format : 'on' atau 'off' (menggunakan petik)")


args = parser.parse_args()
cookie=args.cookie
print('Cookie yang digunakan : ' + cookie)
semester=args.semester
print('Semester yang dipilih : ' + semester)
report=args.report
print('Report : ' + report)


print('\n')

# exit()

header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'Cookie': 'PHPSESSID=' + cookie,
         'Connection':'keep-alive',
         'Cache-Control' : 'max-age=0',
         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
         'Host':'private-feeder.ulm.ac.id',
         'Accept-Encoding':'gzip, deflate'
         }
payload = {'jenis_chart': 'jumlahmhsnonakm',
           'id_smt': semester}

d = FeederScraper(url, header, payload, report)
d.main()






