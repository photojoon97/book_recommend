"""
--------------------------------------
Created on Fri May 21 02:18:38 2021

@author: SooYeon Yim(team7, UFO/2020039017)

Description:a web crawler that scraps book titles and introduction(abstract) data from Naver Book Home

Name:GetData
--------------------------------------
"""

import csv
# 설치한 selenium에서 webdriver를 import
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip

from selenium.webdriver.chrome.options import Options

import requests

def clipboard_input(user_xpath, user_input):
        temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

        pyperclip.copy(user_input)
        driver.find_element_by_xpath(user_xpath).click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
        time.sleep(1)
        
def book_crawling(driver):
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
           
           book_info.append([title,url])
       return book_info
                

def save_data(book_info):
        csvFile=open("C:/Users/yimso/Downloads/etc/noveltest.csv",'wt',encoding='utf-8-sig',newline='')#a옵션...
        writer=csv.writer(csvFile)
        columns=['title','abstract']
        writer.writerow(columns)
        try:
            writer.writerows(book_info)
        finally:
            csvFile.close
            
def url():
    csvfile = open('C:/Users/yimso/Downloads/etc/url.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(csvfile)
    for line in rdr:
        url_list.append(line)
    
    csvfile.close()
    return url_list    
        

if __name__ == "__main__":
        driver = webdriver.Chrome(r'C:\Users\yimso\Downloads\chromedriver.exe')
        # 접속할 url
        Url = 'https://nid.naver.com/nidlogin.login'

        # 접속 시도
        driver.get(Url)
        login = {
            "id" : "testid",
            "pw" : "testpw"
            }
        
        # 아이디와 비밀번호를 입력합니다.
        time.sleep(1)
        clipboard_input('//*[@id="id"]', login.get("id"))
        
        time.sleep(1.5) 
        clipboard_input('//*[@id="pw"]', login.get("pw"))
        driver.find_element_by_xpath('//*[@id="log.login"]').click()

        book_info=[]
        book_info_list=[]
        url_list=[]
        for i in range(1,195):
            try:
                l=url()
                
                for page in range(1,6):
                    utx=str(l[i]).replace("['", "")
                    utx1=utx.replace("']", "")
                    
                    url=utx1+str(page)
                    time.sleep(0.5)
                    url='http://book.naver.com/category/index.nhn?cate_code=100010010&tab=top100&list_type=list&sort_type=publishday&page='+str(page)
                    driver.implicitly_wait(30)
                    
                    driver.get(url)
                    d=book_crawling(driver)
                    book_info_list=d
                    save_data(book_info_list)
                    time.sleep(1)
            
            except:
                print('done')


    

    
        





    

