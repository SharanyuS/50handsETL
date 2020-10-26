# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 08:59:25 2020

@author: askewoperative
"""

from selenium import webdriver
import time
import pymysql
import csv
import os
import pandas as pd

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

    #conn = pymysql.connect(host='localhost', user='root', password='Shri2003:)', db='covid_data')
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
    
browser.get("https://www.canada.ca/content/dam/eccc/documents/csv/cesindicators/water-quality-canadian-rivers/2020/wqi-iqe-federal-score-2020.csv")
print('ok')
#time.sleep(3)
#browser.find_element_by_xpath("/html/body/main/div[1]/div[2]/div/ul/li[7]/div/a").click()
#time.sleep(2)
#print('ok')
#browser.find_element_by_class_name("Federal water quality index scores").click()
#time.sleep(1)

with open('wqi-iqe-federal-score-2020.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('ca_water_pollution.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)

upload_to_SQL('ca_water_pollution.csv', 31, "s3_ca_water_pollution")  

os.remove('wqi-iqe-federal-score-2020.csv')      