import csv
import sys
from collections import Counter
import re

def remov_duplicates(input):
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
def lower_rd_r2(input):
    input_new = input[0].lower()
    input_new = remov_duplicates(input_new)
    input_new = input_new.replace("-", " ")
    input_new = re.sub(r'\b\w{1,2}\b', '', input_new).lstrip(' ')
    return input_new

#input number you want to search

# csv prodi feeder
prodi_csv = csv.reader(open('prodi_sample.csv', "rt",  encoding='utf-8'), delimiter=",")

#loop through csv list
jumlah_prodi = 0
jumlah_fakultas = 0
# loop list prodi dari feeder
for pro in prodi_csv:
    prodi_new = lower_rd_r2(pro)
    print(prodi_new)

    # csv dari database sia_m_prodi relasi sia_m_fakultas
    prodixfakultas = csv.reader(open('prodixfakultas.csv', "rt", encoding='utf-8'), delimiter=",")
    for row in prodixfakultas:
        if prodi_new in row[0].lower():
            jumlah_fakultas += 1 # jumlah prodi ulm
            print(row[1])
            break
    jumlah_prodi+=1 # jumlah prodi feeder
    print('\n')
print("jumlah fakultas : "+str(jumlah_fakultas))
print("jumlah prodi : "+str(jumlah_prodi))
