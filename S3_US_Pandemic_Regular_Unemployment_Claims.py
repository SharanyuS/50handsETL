# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:41:43 2020

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

browser.get("https://oui.doleta.gov/unemploy/claims.asp")
time.sleep(3)
browser.find_element_by_css_selector("input[type='radio'][value='xls']").click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/table/tbody/tr[6]/td/input').click()

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

with open('r539cy.xls') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('clean.html', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)
            
df=pd.DataFrame()
df=pd.read_html('clean.html')

df1=pd.DataFrame()
df1=df[0]

df1.to_csv('Pandemic_Regular_Unemployment_Claims.csv',header=0,index=False)

df1= pd.read_csv('Pandemic_Regular_Unemployment_Claims.csv')


cols = df1.iloc[:2].fillna('')

df1.columns = (cols.iloc[0] + ' ' + cols.iloc[1]).str.strip()
df1.columns.values[0] = 'Date'

df1 = df1.iloc[2:]
df1.to_csv('Pandemic_Regular_Unemployment_Claims.csv',index=0)       

upload_to_SQL('Pandemic_Regular_Unemployment_Claims.csv', 12, 'US_Pandemic_Regular_Unemployment_Claims')

os.remove('r539cy.xls')
os.remove('clean.html')