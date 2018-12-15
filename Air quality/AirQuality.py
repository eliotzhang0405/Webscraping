# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 18:30:24 2018

@author: Zhang Yiming
"""

import bs4 as bs
import requests
import pandas as pd
from selenium import webdriver
import re
from tqdm import tqdm
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



url = 'https://www.aqistudy.cn/historydata/'

browser = webdriver.Chrome(executable_path=r'D:\AFPD\Projects\My code\10. webscraping\chromedriver.exe')
browser.maximize_window()
browser.implicitly_wait(10)

url_city_form = 'https://www.aqistudy.cn/historydata/monthdata.php?city={}'
#Find the name of all the cities#
browser.get(url)
total = browser.find_elements_by_xpath('//div[@class = \'all\']/div[@class = \'bottom\']/ul/div/li')
city_list = []
result_list = []
for CITY in total:
    city_list.append(CITY.text)
 
#For each city, find all the information#
for city_count in tqdm(city_list):    
    browser.get(url_city_form.format(city_count))
    try : 
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH,'//table/tbody/tr[2]')))
        city_detail = browser.find_elements_by_xpath('//tbody')[0].text.split('\n')[1:]
        for i in range(int(len(city_detail)/3)):
            City = city_count
            Year = city_detail[3*i+0].split(' ')[0][:4]
            Month = city_detail[3*i+0].split(' ')[0][5:]
            AQI = city_detail[3*i+0].split(' ')[1]
            Range = city_detail[3*i+0].split(' ')[2].split('\n')[0]
            Air_quality_level = city_detail[3*i+1]
            Air_PM25 = city_detail[3*i+2].split(' ')[0]
            Air_PM10 = city_detail[3*i+2].split(' ')[1]
            Air_SO2 = city_detail[3*i+2].split(' ')[2]
            Air_CO = city_detail[3*i+2].split(' ')[3]
            Air_NO2 = city_detail[3*i+2].split(' ')[4]
            Air_O3 = city_detail[3*i+2].split(' ')[5]
            result_list.append([City, Year, Month, AQI, 
                                Range, Air_quality_level, Air_PM25, 
                                Air_PM10, Air_SO2, Air_CO, Air_NO2, Air_O3])
    except :
        continue
#Gather the information in one Dataframe#    
df_total = pd.DataFrame(result_list, columns = ['City',
                                   'Year', 
                                   'Month',
                                   'AQI',
                                   'Range',
                                   'Air Quality level',
                                   'PM2.5',
                                   'PM10',
                                   'SO2',
                                   'CO',
                                   'NO2',
                                   'O3'])
#Out put the dataframe#
df_total.to_csv(r'D:\AFPD\Projects\My code\10. webscraping\Air quality\Air_quality.csv',encoding="utf-8-sig")