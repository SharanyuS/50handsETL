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

browser.get("http://api.worldbank.org/v2/en/country/USA?downloadformat=excel")
"""time.sleep(7)
print("ok")
browser.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div[1]/article/aside/div/div/div/p/div/a").click()
time.sleep(1)
print("ok")"""

df=pd.DataFrame()
df=pd.read_excel("API_USA_DS2_en_excel_v2_1217999.xls",sheet_name="Data",index=False)
print("ok")
#print(df)
df.drop(df.index[[0,1]],inplace=True)
df.drop(df.columns[0],axis=1)

df.to_csv('us_interest_rate.csv', encoding='utf-8', index=False,header=0)
print("ok")
with open('us_interest_rate.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('s3_us_interest_rate.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)
print("ok")
df2=pd.read_csv('s3_us_interest_rate.csv')
print(df)
            

upload_to_SQL('s3_us_interest_rate.csv', 64, "s3_us_interest_rate")

os.remove('us_interest_rate.csv')
os.remove('API_USA_DS2_en_excel_v2_1217999.xls')
