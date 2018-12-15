# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 21:13:03 2018

@author: Zhang Yiming
"""
import bs4 as bs
import requests
import pandas as pd
from selenium import webdriver
import re
from time import sleep

browser = webdriver.Chrome(executable_path=r'D:\AFPD\Projects\My code\10. webscraping\chromedriver.exe')

#Let the user input necessary information#
information = input('Please enter the date to check in(yyyy-mm-dd), the date to check out(yyyy-mm-dd), the location to check in, the number of children to check in, the number of infants to check in, the number of adults to check in: (separator is \', \')')
inf_list = information.split(', ')

#seperate the information to different programing input#
date_to_check_in = inf_list[0]
date_to_check_out = inf_list[1]
location_to_check_in = inf_list[2]
number_of_children_to_check_in = inf_list[3]
number_of_infants_to_check_in = inf_list[4]
number_of_adults_to_check_in = inf_list[5]
original_form = 'https://www.airbnbchina.cn/s/homes?refinement_paths%5B%5D=%2Fhomes&checkin={}&checkout={}&adults={}&children={}&infants={}&toddlers=0&query={}'
url = original_form.format(date_to_check_in, date_to_check_out, number_of_adults_to_check_in, number_of_children_to_check_in, number_of_infants_to_check_in, location_to_check_in)

browser.get(url)
sleep(5)
soup = bs.BeautifulSoup(browser.page_source, 'lxml')
div = soup.find('div', {'class': 'search-results'})
df_total = pd.DataFrame(columns = ['Space type of the room',
                                   'The number of beds',
                                   'The number of bedrooms',
                                   'The number of Bathrooms',
                                   'Name of the room',
                                   'Currency',
                                   'The way of charging',
                                   'Where room at',
                                   'The level of star',
                                   'ID for the room',
                                   'Amount of viewer',
                                   'Price of room'])



#Find the url for all the room#
url_room = ['https://' + x.get('content') for x in div.findAll('meta',{'itemprop':'url'})]

#Find all the information of one room#
for room in url_room:
    browser.get(room)
    sleep(5)
    room_soup =bs.BeautifulSoup(browser.page_source, 'lxml')
    room_type = room_soup.findAll('span',{'class':'_ju40xgb'})[1].find('span').text
    room_number_of_beds =room_soup.findAll('span',{'class':'_eamm1ge'})[1].text
    room_number_of_bedrooms = room_soup.findAll('span',{'class':'_eamm1ge'})[0].text
    room_number_of_bathrooms = room_soup.findAll('span',{'class':'_eamm1ge'})[2].text
    room_name = room_soup.find('h1',{'class':'_14i3z6h'}).text
    try: 
        room_currency = re.sub('\d','',room_soup.find('span',{'class':'_doc79r'}).text)[0]
    except AttributeError: 
        room_currency = re.sub('\d','',room_soup.find('span',{'class':'_1er4lvly'}).text)[0]
    try: 
        room_price = re.sub('\D','',room_soup.find('span',{'class':'_doc79r'}).text)
    except AttributeError: 
        room_price = re.sub('\D','',room_soup.find('span',{'class':'_1er4lvly'}).text)
    room_the_way_of_charing = room_soup.find('span',{'class':'_1cy09umr'}).text
    room_where_room_at = room_soup.find('div',{'class':'_190019zr'}).text
    try: 
        room_the_level_of_stars = room_soup.find('span',{'role':'img'}).get('aria-label')
    except AttributeError:
        room_the_level_of_stars = 'Not available'
    room_id = re.sub('\D','', room[32:41])
    try:
        room_amount_of_reviewers = room_soup.findAll('span',{'class':'_1cy09umr'})[1].text
    except IndexError:
        room_amount_of_reviewers = 'Not available'
    room_detail = [room_type, room_number_of_beds, room_number_of_bedrooms, room_number_of_bathrooms, room_name, room_currency, room_the_way_of_charing, room_where_room_at, room_the_level_of_stars, room_id, room_amount_of_reviewers, room_price]
    df_total.loc[len(df_total)+1] = room_detail
#Output the data#    
df_total.to_excel(r'D:\AFPD\Projects\My code\10. webscraping\Airbnb\results.xlsx')