# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 18:47:52 2020

@author: askewoperative
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql
import os

url = 'https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=18992'
r = requests.get(url, allow_redirects=True)

open('IN_household_disposable_income.html', 'wb').write(r.content)
soup = BeautifulSoup(r.content, 'lxml')
table = soup.find_all('table')[0]
    
df = pd.DataFrame()

df = pd.read_html(str(table))

df[1].drop(df[1].tail(1).index,inplace=True)

df[1].drop(df[1].head(2).index,inplace=True)
dft=df[1].T

dft.to_csv("in_housing_disposable_income.csv",header=0, index=False)

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
    #conn = pymysql.connect(host='localhost',user='root',password='sharanyu',db='plsbefast')
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

upload_to_SQL('in_housing_disposable_income.csv', 23, "in_housing_disposable_income")   
os.remove('IN_household_disposable_income.html') 