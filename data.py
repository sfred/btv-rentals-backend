import csv
from urllib import *
import ssl
import requests
import re
from bs4 import BeautifulSoup
import pandas
from datetime import datetime
import psycopg2

#URL for Heroku -> Database for environment
#drop VALUES



def create_table():
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor2 = connection.cursor()
    cursor2.execute("CREATE TABLE rental_comp(coc_years smallint, coc_issue_date date, coc_expire_date date, span text, street_address text, unit_number text, land_use_code text, residential_units bigint, rental_units bigint, tax_parcel_id text, update_date date)")
    connection.commit()


def insert_data(row):
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO rental_practice VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", row)
    connection.commit()

def find_span(span):
    if span in spans:
        return True
    else:
        spans.append(span)
        return False

def read_csv():
    csv_file = requests.get('https://data.burlingtonvt.gov/explore/dataset/rental-property-certificate-of-compliance/download?format=csv')
    csv_decoded = csv_file.content.decode('utf-8')
    csv_reader = csv.reader(csv_decoded.splitlines())
    list_rows = list(csv_reader)
    headers = list_rows[0]
    print(headers)
    for i in range (1,len(list_rows)):
        if(len(list_rows[i]) < 2):
            row = list_rows[i][0].split(';')
            # print(i + row)
        else:
            row_temp = list_rows[i][0].split(';')
            row_temp1 = list_rows[i][1].split(';')
            row = row_temp
            row.append(row_temp1[0])
            # print(i + row)
        insert_row = []
        for j in range(len(row)):
             if(row[j] == ''):
                 if(j != 9 and j!= 12 and j!=13):
                     if(j == 3):
                         del(insert_row)
                         print("Row Dropped: "+ row[4])
                         insert = False
                         break
                     else:
                         # print("Row: "+ str(i)) print("Column: "+ str(j))
                         insert_row.append(None)
             else:
                 if(j == 0 or j == 7 or j == 8 or j == 11):
                     insert_row.append(int(row[j]))
                 elif(j == 1 or j == 2 or j == 14):
                     insert_row.append(datetime.strptime(row[j], '%Y-%m-%d'))
                 elif(j == 4 or j == 5 or j == 6 or j == 10 or j ==15):
                       if(j == 15):
                           insert_row.append(row[15]+ ", "+ row[16])
                           insert = True
                       else:
                           insert_row.append(row[j])
                 elif(j == 3):
                     found = find_span(row[j])
                     if(found):
                         del(insert_row)
                         print("Row Dropped: "+ row[3] + " " + row[4])
                         insert = False
                         break
                     else:
                         insert_row.append(row[j])
        # if(insert):
        #     # print(" ")
        #     # print(i)
        #     insert_data(insert_row)
        #     # print(insert_row)
        #     # print(" ")


def main():
   userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
   create_table()
   read_csv()
   

main()
