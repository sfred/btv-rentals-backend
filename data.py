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



def create_practice():
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor2 = connection.cursor()
    cursor2.execute("CREATE TABLE rental_comp(coc_years smallint, coc_issue_date date, coc_expire_date date, span text, street_address text, unit_number text, land_use_code text, residential_units bigint, rental_units bigint, tax_parcel_id text, update_date date)")
    connection.commit()



def insert_data(row):
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO rental_comp VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", row)
    connection.commit()


def main():
   userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
   data_url = 'https://data.burlingtonvt.gov/explore/dataset/rental-property-certificate-of-compliance/export/?sort=residentialunits'
   page_text = BeautifulSoup(requests.get(data_url).text, features="lxml")

   # excel = pandas.read_excel('https://data.burlingtonvt.gov/explore/dataset/rental-property-certificate-of-compliance/download?format=xls')
   excel = BeautifulSoup(requests.get('https://data.burlingtonvt.gov/explore/dataset/rental-property-certificate-of-compliance/download?format=xls').text, features="lxml")
   # print(excel.prettify())
   # for row in excel.find_all('row'):
   #     row = []
   #     for cell in row.find_all('cell'):
   #         for data in cell.find_all('data'):
   #             print data.text,
   #     print()

   create_practice()

   for row in excel.find_all('row'):
       r  = []
       counter = 0
       for cell in row.find_all('cell'):
           if(cell.get('ss:index') == "1") :
               text = cell.find('data').text
               r.append(int(text))
               counter +=  1
               # print cell.find('data').text,
           # CoCIssueDate
           elif(cell.get('ss:index')== "2"):
               r.append(datetime.strptime(cell.find('data').text, '%Y-%m-%d'))
               counter += 1
               # for data in cell.find_all('data'):
               #   print cell.find('data').text,
           #CoCExpireDate
           elif(cell.get('ss:index')== "3"):
               r.append(datetime.strptime(cell.find('data').text, '%Y-%m-%d'))
               counter += 1
               # r.append(cell.find('data').text)
               # for data in cell.find_all('data'):
               #   print cell.find('data').text,
           #Span
           elif(cell.get('ss:index')== "4"):
               while(counter < 3):
                   r.append(None)
                   counter += 1
               r.append(str(cell.find('data').text))
               counter += 1
               # for data in cell.find_all('data'):
               #   print cell.find('data').text,
         #Address
           elif(cell.get('ss:index')== "5"):
               while(counter < 4):
                    r.append(None)
                    counter += 1
               r.append(str(cell.find('data').text))
               counter += 1
               # for data in cell.find_all('data'):
               #    print data.text,
         #Unit Number
           elif(cell.get('ss:index')== "6"):
               # if(len(str(cell.find('data').text)) == 0):
               #     r.append(' ')
               # else:
               #  print("Unit Number: " + str(cell.find('data').text))
               while(counter < 5):
                   r.append(None)
                   counter += 1
               r.append(str(cell.find('data').text))
               counter += 1
               # for data in cell.find_all('data'):
               #   print cell.find('data').text,
        #LandUseCode
           elif(cell.get('ss:index')== "7"):
               while(counter < 6):
                    r.append(None)
                    counter += 1
               r.append(str(cell.find('data').text))
               counter += 1
               # for data in cell.find_all('data'):
               #   print data.text,
         #ResidentialUnits
           elif(cell.get('ss:index')== "8"):
               while(counter < 7):
                    r.append(None)
                    counter += 1
               r.append(int(cell.find('data').text))
               counter += 1
               # for data in cell.find_all('data'):
               #   print data.text,
         #RentalUnits
           elif(cell.get('ss:index')== "9"):
               while(counter < 8):
                    r.append(None)
                    counter += 1
               r.append(int(cell.find('data').text))
               counter +=1
               # for data in cell.find_all('data'):
               #   print data.text,
         #TaxParcelIds
           elif(cell.get('ss:index')== "11"):
               # if(counter < 10):
               #      r.append('NULL')
               r.append(str(cell.find('data').text))
               counter += 1
               # for data in cell.find_all('data'):
               #    print data.text,
           elif(cell.get('ss:index')== "15"):
               # if(counter < 15):
               #     r.append('NULL')
                   # counter += 1
               r.append(datetime.strptime(cell.find('data').text, '%Y-%m-%d'))


       # if(len(r) != 11):
       #     print(len(r))
       #     print(r)

       if(len(r) == 11):
           insert_data(r)

       # print("Length: " +str(len(r)))
       # print(r)
       # insert_data(r)





main()
