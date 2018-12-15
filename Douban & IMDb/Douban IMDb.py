# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:58:21 2018

@author: Zhang Yiming
"""
import bs4 as bs
import requests
import pandas as pd
from selenium import webdriver
import re
from time import sleep


#textinput = '肖申克的救赎,Shawshank,大英雄,111'
movie_list = input('Please type in the name of the movie, separater: \',\': ').split(',')
search_type = int(input('Please type the search type(1 for Douban, 2 for IMDd): '))
df_not_found = pd.DataFrame(['Moive not found'])
browser = webdriver.Chrome(executable_path=r'D:\AFPD\Projects\My code\10. webscraping\chromedriver.exe')

#Webscraping for Douban#
if search_type == 1: 
    url_Douban_form = 'https://movie.douban.com/top250?start={}&filter='
    df_total_douban = pd.DataFrame(columns = ['The name of movie',
                                       'The release date',
                                       'The directors',
                                       'The main actors/actresses',
                                       'The average rating score',
                                       'The total amount of people rating',
                                       'The brief introduction'])
    #Get all the data of all top 250 movie and generate a local dataframe#
    for counter in range(0,250,25):
        browser.get(url_Douban_form.format(counter))
        xpath = '//div[@class = \'item\']'
        for item in browser.find_elements_by_xpath(xpath):
            movie_name = re.sub(' \[可播放\]','',item.text.split('\n')[1])
            movie_release_date = re.sub('\D','',item.text.split('\n')[3])
            movie_director = item.text.split('\n')[2].split('   ')[0]
            try:
                movie_main = item.text.split('\n')[2].split('   ')[1].split('...')[0] + '...'
            except IndexError: 
               movie_main =  'not available'
            movie_average_rate = item.text.split('\n')[4][0:3] + '/10' 
            movie_amount = item.text.split('\n')[4][4:]
            try:
                movie_intro = item.text.split('\n')[5]
            except IndexError: 
                movie_intro = 'not available'
            movie_detail = [movie_name, movie_release_date, movie_director, movie_main, movie_average_rate, movie_amount, movie_intro]
            df_total_douban.loc[len(df_total_douban)+1] = movie_detail
    df_total_douban.to_csv(r'D:\AFPD\Projects\My code\10. webscraping\Douban & IMDb\result\Douban.csv',encoding="utf-8-sig", index = False)
    #search whether the movie is in the local dataframe, output the data if in and output not found if not#
    for name_search in movie_list:
        in_or_not = 0
        for i in range(1,251):
            if name_search in df_total_douban['The name of movie'][i]:
                df_total_douban.loc[i].to_csv(r'D:\AFPD\Projects\My code\10. webscraping\Douban & IMDb\result'+'\\' + name_search + '.csv',encoding="utf-8-sig", index = True)
                in_or_not = 1
            elif i == 250 and in_or_not == 0:
                df_not_found.to_csv(r'D:\AFPD\Projects\My code\10. webscraping\Douban & IMDb\result'+'\\' + name_search + '.csv',encoding="utf-8-sig", index = False)
 
#Webscraping for IMDb#           
elif search_type == 2:

    url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
    browser.get(url)
    xpath_IMDb = '//td[@class = \'titleColumn\']/a'
    browser.find_elements_by_xpath('//td[@class = \'titleColumn\']/a')
    df_total_IMDb = pd.DataFrame(columns = ['The name of movie',
                                       'The release date',
                                       'The directors',
                                       'The main actors/actresses',
                                       'The average rating score',
                                       'The total amount of people rating',
                                       'The brief introduction'])
    
    movie_total_IMDd = []
    for item_IMDd in browser.find_elements_by_xpath('//td[@class = \'titleColumn\']/a'):
        movie_total_IMDd.append(item_IMDd.text)
    #Check whether the movie is in the top 250#    
    for name_search in movie_list:
        browser.get(url)
        in_or_not = 0
        for i in range(250):
            #if the movie is in, output all the required data#
            if name_search in movie_total_IMDd[i]:
                page_num = i
                browser.find_elements_by_xpath('//td[@class = \'titleColumn\']/a')[page_num].click() 
                movie_name = browser.find_elements_by_xpath('//div[@class = \'title_wrapper\']/h1')[0].text.split(' (')[0]
                movie_release_date = browser.find_elements_by_xpath('//div[@class = \'title_wrapper\']/h1')[0].text.split(' (')[1][:4]
                movie_director = browser.find_elements_by_xpath('//div[@class = \"credit_summary_item\"]')[0].text.split(': ')[1]
                movie_main = browser.find_elements_by_xpath('//div[@class = \"credit_summary_item\"]')[2].text.split(': ')[1].split('|')[0]
                movie_average_rate = browser.find_elements_by_xpath('//span[@itemprop = \"ratingValue\"]')[0].text + '/10'
                movie_amount = browser.find_elements_by_xpath('//span[@itemprop = \"ratingCount\"]')[0].text 
                movie_intro = browser.find_elements_by_xpath('//div[@class = \"summary_text\"]')[0].text
                movie_detail = [movie_name, movie_release_date, movie_director, movie_main, movie_average_rate, movie_amount, movie_intro]
                df_total_IMDb.loc[1] = movie_detail
                df_total_IMDb.loc[1].to_csv(r'D:\AFPD\Projects\My code\10. webscraping\Douban & IMDb\result'+'\\' + name_search + '.csv',encoding="utf-8-sig", index = True)
                in_or_not = 1
        #If the movie is not in, output movie not found#        
        if in_or_not == 0:
            df_not_found.to_csv(r'D:\AFPD\Projects\My code\10. webscraping\Douban & IMDb\result'+'\\' + name_search + '.csv',encoding="utf-8-sig", index = False)
    
else:
    print ('Search type error, please restart')











