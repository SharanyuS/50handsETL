from selenium import webdriver
import time
import pymysql
import csv
import os

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

    
    conn = pymysql.connect(host='34.89.97.3', user='u831388458_covid19', password='Password@123', db='u831388458_covid19stats')
    #conn = pymysql.connect(host='localhost',user='root',password='sharanyu',db='covid_db')
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

#chrome_path = r"/Users/askewoperative/Desktop/50hands/chromedriver"
chrome_path = r"/usr/bin/chromedriver"

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

browser.get("https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1010012701&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=1951&cubeTimeFrame.endMonth=12&cubeTimeFrame.endYear=2020&referencePeriods=19510101%2C20201201")
time.sleep(3)
browser.find_element_by_xpath("/html/body/main/form/div[3]/a[3]").click()
time.sleep(1)
browser.find_element_by_xpath("/html/body/div[2]/div/div[1]/section/div[1]/div[1]/div/div[3]/a").click()
time.sleep(1)

with open('1010012701_databaseLoadingData.csv') as rf:
    csv_reader=csv.reader(rf)
    # next(rf)
    with open('ca_foreign_exchange_reserve.csv', 'w', newline='') as wf:
        mywriter = csv.writer(wf)
        for d in csv_reader:
            for i in range(0,len(d)):
                res = [sub.replace(',', '') for sub in d]
                res2 = [sub.replace('\'', '') for sub in res]
                res3= [sub.replace('\\', '') for sub in res2]
                res4 = [sub.replace('\"', '') for sub in res3]
            mywriter.writerow(res4)

upload_to_SQL('ca_foreign_exchange_reserve.csv', 15, "ca_foreign_exchange_reserves")

os.remove('1010012701_databaseLoadingData.csv')
