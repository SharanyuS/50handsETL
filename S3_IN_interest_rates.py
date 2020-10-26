# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 13:34:45 2020

@author: askewoperative
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql
import os

url = 'https://countryeconomy.com/key-rates/india'
r = requests.get(url, allow_redirects=True)

open('IN_interest_rates.html', 'wb').write(r.content)
soup = BeautifulSoup(r.content, 'lxml')
table = soup.find_all('table')[0]

df = pd.DataFrame()

df = pd.read_html(str(table))[0]

df.index=df.index+1

df['Key rates']=df['Key rates'].str[:-1].astype(float)
df.index.names = ['index']

df.to_csv("IN_interest_rates.csv", index=True)

def upload_to_SQL(path_to_csv, num_cols, table_name):
    f = open(path_to_csv, "r")
    fString = f.read()
    fList = []
    for line in fString.split('\n'):
        fList.append(line.split(','))
    row_part = "('{}'"
    for c in range(0,num_cols-1):
        row_part += ",'{}'"
    row_part += ")"
    #conn = pymysql.connect(host='localhost',user='root',password='sharanyu',db='covid_db')
    conn = pymysql.connect(host='34.89.97.3', user='u831388458_covid19', password='Password@123', db='u831388458_covid19stats')
    print("Opened database successfully")
    cursor = conn.cursor()
    query = "DELETE FROM " + table_name
    cursor.execute(query)
    conn.commit()
    rows = ""
    for i in range(1, len(fList) - 1):
        param_list = []
        for j in range(0, num_cols):
            param_list.append(str(fList[i][j]))
        rows += row_part.format(*param_list)
        if i != len(fList) - 2:
            rows += ','
    queryInsert = "INSERT INTO " + table_name + " VALUES " + rows
    cursor.execute(queryInsert)
    conn.commit()
    print("Uploaded")
    conn.close()
 
upload_to_SQL('IN_interest_rates.csv',3,'s3_in_interest_rates')  
os.remove('IN_interest_rates.html')