# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:00:31 2020

@author: askewoperative
"""

from selenium import webdriver
import time
import pymysql
import csv
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from selenium.webdriver import ActionChains

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

    # conn = pymysql.connect(host='localhost', user='root', password='Shri2003:)', db='covid_data')
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

chrome_path = r"/Users/askewoperative/Desktop/50hands/chromedriver"

preferences = {"download.default_directory": "/Users/askewoperative/Desktop/50hands"}


chrome_options= webdriver.ChromeOptions()
chrome_options.EnsureCleanSession = True
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-notifications')
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("prefs", preferences)
browser = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

browser.get("https://www.bea.gov/sites/default/files/2020-07/gdp2q20_adv.xlsx")
time.sleep(3)

df=pd.DataFrame()
df=pd.read_excel('gdp2q20_adv.xlsx',sheet_name='Table 3')

df.to_csv('convert3.csv')

with open('convert3.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('US_GDP_table_3.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)
            
df=pd.read_csv('US_GDP_table_3.csv',header=None)

df=df.iloc[1:]
df.drop(df.tail(4).index,inplace=True)

df.drop(df.columns[[0,1]], axis=1, inplace=True)

cols = df.iloc[:4].fillna('')

df.columns = (cols.iloc[0] + ' ' + cols.iloc[1]+' '+cols.iloc[2]+' '+cols.iloc[3]).str.strip()

df=df.iloc[4:]

df.rename( columns={'':'GDP: changes from preceding years'}, inplace=True)
df.rename(columns={"Billions of dollars 2019 2019 2019": "Billions($) 2019", "Billions of dollars Seasonally adjusted at annual rates 2019 Q2": "Seasonally adjusted at annual rates 2019 Q2 bn($)","Billions of dollars Seasonally adjusted at annual rates 2019 Q3":"Seasonally adjusted at annual rates 2019 Q3 bn($)","Billions of dollars Seasonally adjusted at annual rates 2019 Q4":"Seasonally adjusted at annual rates 2019 Q4 bn($)","Billions of dollars Seasonally adjusted at annual rates 2020 Q1":"Seasonally adjusted at annual rates 2020 Q1 bn($)","Billions of dollars Seasonally adjusted at annual rates 2020 Q2":"Seasonally adjusted at annual rates 2020 Q2 bn($)","Billions of chained (2012) dollars 2019 2019 2019":"bn($) of chained (2012) dollars 2019","Billions of chained (2012) dollars Seasonally adjusted at annual rates 2019 Q2":"bn of chained($)(2012) Seasonally adjusted annual rates 2019Q2","Billions of chained (2012) dollars Seasonally adjusted at annual rates 2019 Q3":"bn of chained($)(2012) Seasonally adjusted annual rates 2019Q3","Billions of chained (2012) dollars Seasonally adjusted at annual rates 2019 Q4":"bn of chained($)(2012) Seasonally adjusted annual rates 2019Q4","Billions of chained (2012) dollars Seasonally adjusted at annual rates 2020 Q1":"bn of chained($)(2012) Seasonally adjusted annual rates 2020Q1","Billions of chained (2012) dollars Seasonally adjusted at annual rates 2020 Q2":"bn of chained($)(2012) Seasonally adjusted annual rates 2020Q2","Billions of chained (2012) dollars Change from preceding period 2019 2019":"bn($) of chained (2012) Change from preceding period 2019","Billions of chained (2012) dollars Change from preceding period 2020 Q1":"bn of chained($)(2012)change from preceding year 2020Q1","Billions of chained (2012) dollars Change from preceding period 2020 Q2":"bn of chained($)(2012)change from preceding year 2020Q2"},inplace=True)

df.to_csv('US_GDP_table_3.csv',index=False) 

upload_to_SQL('US_GDP_table_3.csv', 16, 'US_GDP_table_3')

os.remove('gdp2q20_adv.xlsx')
os.remove('convert3.csv')