# untuk excel
import csv
# untuk cprint
import sys
# untuk math operation
import math
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
# for remov_duplicates() function
from collections import Counter
# for lower_rd_r2() function
import re
from konfigurasi_ini import default_cookie,default_semester,default_report,default_useragent

# print (default_cookie)
# print (default_semester)
# print (default_report)
# print (default_useragent)
#
# exit()
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

    def remove_duplicates(self, input):
        # split input string separated by space
        input = input.split(" ")

        # joins two adjacent elements in iterable way
        for i in range(0, len(input)):
            input[i] = "".join(input[i])

            # now create dictionary using counter method
        # which will have strings as key and their
        # frequencies as value
        UniqW = Counter(input)

        # joins two adjacent elements in iterable way
        s = " ".join(UniqW.keys())
        return s

    # lowering, remove duplicate words, remove 2 letter words
    def lower_rd_r2(self, input):
        input_new = input.lower()

        # selain 'pendidikan' tidak boleh duplikat
        if 'pendidikan' not in input_new:
            input_new = self.remove_duplicates(input_new)

        input_new = input_new.replace("-", " ")
        input_new = input_new.replace("-", " ")

        input_new = re.sub(r'\b\w{1,2}\b', '', input_new).lstrip().rstrip()
        return input_new

    def get_fakultas(self, input):
        # csv prodi feeder
        prodi_new = self.lower_rd_r2(input)
        # print(prodi_new)
        fakultas = " ";
        # csv dari database sia_m_prodi relasi sia_m_fakultas
        prodixfakultas = csv.reader(open('prodixfakultas.csv', "rt", encoding='utf-8'), delimiter="=")
        for row in prodixfakultas:
            if prodi_new in row[0].lower():
                fakultas = row[1]
                break
        return fakultas

    # membulatkan keatas
    def roundup(self, x):
        return int(math.ceil(x/10)*10)

    # remove in string except alphabet and numeric
    def remove_except_intstring(self,string):
        return ''.join(e for e in string if e.isalnum())

    def e(self):
        sys.exit()
        
    def login_check(self,soup_object):
        is_login = soup_object.findChildren('input', {"value": "Login"})
        if (len(is_login) > 0):
            print('Otentikasi bermasalah.')
            return 0
        else:
            return 1

    def get_total_page(self):
        session = requests.Session()
        available = 0
        total_page = 0
        try:
            result = session.post(self.url, headers=self.header, data=self.payload)
            if result.status_code != 200:
                print('Error ' + str(result.status_code));
                sys.exit()
            else:
                src = result.content
                soup = BeautifulSoup(src, features="html.parser")

                # cek otentikasi
                if(self.login_check(soup)==0):
                    return None

                pagination = soup.findChildren('em')
                if (len(pagination) == 2):
                    my_pagination = pagination[1]
                    total_page = my_pagination.findChildren(['strong'])[2].text
                    total_data = int(self.remove_except_intstring(total_page))
                    total_page = self.roundup(total_data) - 10
                    package = [total_data, total_page]
                    return package
                else:
                    print('Data tidak tersedia - 011X1')
                    return None
        except SystemExit:
            # handling sys.exit
            print("")
            return None
        except session.exceptions.HTTPError as err:
            print('Koneksi gagal')
            return None

    def main(self):
        session = requests.Session()

        # get total page
        total = self.get_total_page()
        if total is not None:
            print('Total Data : '+str(total[0])+' mahasiswa/mahasiswi')
        else:
            sys.exit()

        # initiate csv
        nama_file = 'csv_output_FS_Peserta/' + date.today().strftime(
            "tanggal_%d-%m-%Y") + '_' + datetime.now().strftime("jam_%H-%M-%S") + '.csv'
        file = open(nama_file, 'w', encoding='utf-8', newline='')
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['No', 'Nama', 'NIM', 'Jenis Kelamin', 'Agama', 'Total SKS Diambil', 'Tanggal Lahir', 'Progam Studi', 'Fakultas', 'Status', 'Angkatan'])

        o=0
        o_num =0
        row_num = 0
        print('')
        # pbar = tqdm(total=total_page)
        while o <= total[1]:
            o_num+=1;
            url = self.url + str(o)
            # print(url)
            print('Proses scraping halaman : '+str(o_num)+'/'+str(int((total[1]/10)+1)))
            try:
                result = session.post(url, headers=self.header, data=self.payload)
                if result.status_code != 200:
                    print('Error ' + str(result.status_code));
                    sys.exit()
                else:
                    src = result.content
                    soup = BeautifulSoup(src, features="html.parser")
                    table = soup.findChildren('table', {"class": "table table-striped table-condensed"})
                    my_table = table[1]
                    rows = my_table.findChildren(['tr'])

                    i=0
                    for row in rows:
                        row_data = []
                        if i >= 1:  # 0 dan 1 adalah header dari table
                            row_num += 1
                            columns = row.findChildren(['td'])
                            row_data.append(row_num)
                            row_data.append(columns[1].findChildren(['a'])[0].text)
                            row_data.append(columns[2].text)
                            row_data.append(columns[3].text)
                            row_data.append(columns[4].text)
                            row_data.append(columns[5].text)
                            row_data.append(columns[6].text)
                            row_data.append(columns[7].text)
                            row_data.append(self.get_fakultas(columns[7].text))
                            row_data.append(columns[8].text)
                            row_data.append(columns[9].text)
                            writer.writerow(row_data)
                            # print(columns)

                        i += 1
                # sys.exit()
            except session.exceptions.HTTPError as err:
                pass
            o+=10
            # pbar.update(10)
        # pbar.close()
        print('')
        print('Scraping selesai, silahkan cek file di csv_output_FS_Peserta/'+nama_file)

# Akhir Class FeederScraper

# dieksekusi saat .py dibuka :
url = 'http://private-feeder.ulm.ac.id/pesertadidik/lst/'
print('Private Feeder Scrapper - Peserta Didik')
print('Versi 1.0.0')
print('\n')
print('[*] dimulai @ '+date.today().strftime("/%d-%m-%Y/") + ' ' + datetime.now().strftime("%H:%M:%S"))
print('\n')

# membuat args
parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--cookie", default=default_cookie, help="ini adalah cookie dari aplikasi feeder (PHPSESSID) dengan format : 'COOKIEVALUE' (tanpa petik)")
parser.add_argument("--semester", default=default_semester, help="ini adalah form_data dari aplikasi feeder saat berada dihalaman 'http://private-feeder.ulm.ac.id/home', form_data bisa dilihat melalui Inspect Element, semester dengan contoh format : '20182' (tanpa petik)")
parser.add_argument("--report", default=default_report, help="ini adalah option untuk menampilkan report jumlah baris per-prodi, format : 'on' atau 'off' (tanpa petik)")
parser.add_argument("--useragent", default=default_useragent, help="ini adalah option untuk konfigurasi user agent")

# parsing args
args = parser.parse_args()

cookie=args.cookie
print('Cookie yang digunakan : ' + cookie)
semester=args.semester
print('Semester yang dipilih : ' + semester)
report=args.report
print('Report : ' + report)
useragent = args.useragent
print('Cookie yang digunakan : ' + cookie)


print('\n')

# exit()

header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'Cookie': 'PHPSESSID=' + cookie,
         'Connection':'keep-alive',
         'Cache-Control' : 'max-age=0',
         'User-Agent' : useragent,
         'Host':'private-feeder.ulm.ac.id',
         'Accept-Encoding':'gzip, deflate'
         }
payload = {'jenis_chart': 'jumlahmhsnonakm',
           'id_smt': semester}

# calling main function
d = FeederScraper(url, header, payload, report)
d.main()