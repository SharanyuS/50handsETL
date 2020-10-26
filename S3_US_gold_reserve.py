# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 12:46:30 2020

@author: askewoperative
"""

import pandas as pd
import zipfile
from selenium import webdriver
import time
import pymysql
import csv
import os
import pandas as pd
import numpy as np

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

browser.get("https://fiscaldata.treasury.gov/datasets/status-report-government-gold-reserve/")
time.sleep(3)
browser.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/section[2]/div/div[1]/div[1]/div/label[4]").click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/div/div[1]/div/div[1]/section[2]/div/div[1]/div[2]/div/div[4]/div/div').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[2]/a').click()

zf = zipfile.ZipFile('C:/Users/askewoperative/Desktop/50hands/TreasGold_all_years-20200812.csv.zip') 
df = pd.read_csv(zf.open('TreasGold_all_years.csv'))    

df.to_csv('unzipped.csv',index=False)

with open('unzipped.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('US_gold_reserve.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)
            
            
df1=pd.read_csv('US_gold_reserve.csv')

df1.to_csv("US_gold_reserve.csv",index=False)    
os.remove('unzipped.csv')
        
upload_to_SQL('US_gold_reserve.csv', 13, 'US_gold_reserve')
      
os.remove('TreasGold_all_years.csv')