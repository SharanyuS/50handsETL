# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 11:53:35 2020

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
    
browser.get("https://data.oecd.org/interest/short-term-interest-rates.htm")
print('ok')
time.sleep(3)
browser.find_element_by_xpath("/html/body/div[2]/main/div/main/div/div[3]/div[2]/div/div[1]/ul/li[3]/div/a").click()
time.sleep(3)
print('ok')
browser.find_element_by_class_name("download-indicator-button").click()
time.sleep(1)


with open('DP_LIVE_04082020134335062.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('us_shortterm_interest_rate.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)
            
df=pd.read_csv('us_shortterm_interest_rate.csv')


df["SUBJECT"].replace({"TOT":"Total"}, inplace=True)
df["MEASURE"].replace({"PC_PA":"% per annum"}, inplace=True)
df["FREQUENCY"].replace({"A":"Yearly","M":"Monthly","Q":"Quarterly"},inplace=True)
df["INDICATOR"].replace({"STINT":"Short term interest rate"},inplace=True)

df.to_csv('us_shortterm_interest_rate.csv',index=False)


upload_to_SQL('us_shortterm_interest_rate.csv', 8, "us_shortterm_interest_rate")    