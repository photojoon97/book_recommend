"""
--------------------------------------
Created on Fri May 21 02:18:38 2021

@author: SooYeon Yim(team7, UFO/2020039017)

Description:a web crawler that scraps book titles and introduction(abstract) data from Naver Book Home

Name:GetData
--------------------------------------
"""


import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import time

def book_crawling():
        for page in range(1,6):
            print(page)
            url=move_page(page)
            print(url)
            driver=webdriver.Chrome(ChromeDriverManager().install())#웹드라이버 정의
            driver.implicitly_wait(30) #웹페이지 파싱될때까지 최대 30초 기다림.
            driver.get(url)
            bsObject=BeautifulSoup(driver.page_source,'html.parser')
            book_page_urls=[]
            for index in range(0,20):
                dl_data=bsObject.find('dt',{'id':"book_title_"+str(index)})
                link=dl_data.select('a')[0].get('href')
                book_page_urls.append(link)
                
                
            for index,book_page_url in enumerate(book_page_urls):   
                driver.get(book_page_url)
                bsObject=BeautifulSoup(driver.page_source,'html.parser')
            
                dl_title=bsObject.find('div',{'class':'book_info'})
                title=dl_title.select('a')[0].get_text()
                url=bsObject.find('div',{'id':'bookIntroContent'}).get_text()
                print(title)
                print(url)
                book_info.append([title,url])
                #book_info={title:url}
                #print(book_info[0])
                #print(book_info[1])
                #book_info_list.append(book_info)
        return book_info

def save_data():
        csvFile=open("C:/Users/yimso/Downloads/etc/novel1.csv",'wt',encoding='utf-8-sig',newline='')#a옵션...
        writer=csv.writer(csvFile)
        columns=['title','abstract']
        writer.writerow(columns)
        try:
            #for i in enumerate(book_info):
            writer.writerows(book_info)
        finally:
            csvFile.close


def move_page(page):
        path='http://book.naver.com/category/index.nhn?cate_code=330090&tab=top100&list_type=list&sort_type=publishday&page='+str(page)
        return path



book_info=[]
try:
        book_crawling()
except:
        save_data()    
        





    

