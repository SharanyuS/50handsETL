# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:01:15 2020

@author: askewoperative
"""
from selenium import webdriver
import time
import pymysql
import csv
import os
import pandas as pd

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
#chrome_path = r"/usr/bin/chromedriver"

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

browser.get("http://files.zillowstatic.com/research/public_v2/zori/Metro_ZORI_AllHomesPlusMultifamily_SSA.csv")
time.sleep(1)

with open('Metro_ZORI_AllHomesPlusMultifamily_SSA.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('us_housing_rent_costs.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)
          
df=pd.DataFrame()            
df=pd.read_csv('us_housing_rent_costs.csv')

df['RegionName'] = df['RegionName'].astype(str).str[:-2]

df["RegionName"]=df["RegionName"].str.replace("United Stat","USA")

df_tr=df.transpose()

df_tr.drop('RegionID', axis=0,inplace=True)

df_tr.rename({"RegionName": "Date"}, axis='index',inplace=True)

df_tr.to_csv("us_housing_rental_rates.csv",header=0)



upload_to_SQL('us_housing_rental_rates.csv', 107, "us_housing_rental_rates")

os.remove('us_housing_rent_costs.csv')
os.remove('Metro_ZORI_AllHomesPlusMultifamily_SSA.csv')


