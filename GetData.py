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
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip

def clipboard_input(user_xpath, user_input): #id, password clipboard
        temp_user_input = pyperclip.paste()

        pyperclip.copy(user_input)
        driver.find_element_by_xpath(user_xpath).click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy(temp_user_input)  
        time.sleep(1)
        
def book_crawling(driver): #Crawl book titles and introductions(abstract) through 20(index) book links of url(driver.get(url)) on a page(1~5pages)
       bsObject=BeautifulSoup(driver.page_source,'html.parser')
       book_page_urls=[]
       for index in range(0,20): #collect 20(index) book links
           dl_data=bsObject.find('dt',{'id':"book_title_"+str(index)})
           link=dl_data.select('a')[0].get('href')
           book_page_urls.append(link)
       
       i=0
       while i<20: #collect data through each book link
           try:        
               driver.get(book_page_urls[i])
               bsObject=BeautifulSoup(driver.page_source,'html.parser')
               dl_title=bsObject.find('div',{'class':'book_info'})
               title=dl_title.select('a')[0].get_text()
               url=bsObject.find('div',{'id':'bookIntroContent'}).get_text()
               book_info.append([title,url])
              
           except:
               print('error')
           i=i+1           
       return book_info
                

def save_data(book_info): #save crawling data
        csvFile=open("C:/Users/yimso/Downloads/etc/crawlingdata.csv",'wt',encoding='utf-8-sig',newline='')
        writer=csv.writer(csvFile)
        columns=['title','abstract']
        writer.writerow(columns)
        try:
            writer.writerows(book_info)
        finally:
            csvFile.close
            
def url(): #read (top 100 of each genre)url list 
    csvfile = open('C:/Users/yimso/Downloads/etc/url.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(csvfile)
    for line in rdr:
        url_list.append(line)
    
    csvfile.close()
    return url_list    
        
    

if __name__ == "__main__":
        #Login(to access adult book link)
        driver = webdriver.Chrome(r'C:\Users\yimso\Downloads\chromedriver.exe')
        Url = 'https://nid.naver.com/nidlogin.login'
        driver.get(Url)
        login = {
            "id" : "<<insert your ID>>",
            "pw" : "<<insert your Password>>"
            }
        time.sleep(1) 
        clipboard_input('//*[@id="id"]', login.get("id"))
        time.sleep(1.5)
        clipboard_input('//*[@id="pw"]', login.get("pw"))
        driver.find_element_by_xpath('//*[@id="log.login"]').click()
        
        book_info=[]
        book_info_list=[]
        url_list=[]
        l=url()
        i=0
        while i<195:
            try:
                time.sleep(1)
                for page in range(1,6): # to access 5pages
                    utx=str(l[i]).replace("['", "") # pre-processing url list
                    utx1=utx.replace("']", "")
                    url=utx1+str(page)
                    time.sleep(0.5)
                    driver.implicitly_wait(30)
                    driver.get(url)
                    
                    d=book_crawling(driver)
                    
                    book_info_list=d
                    save_data(book_info_list)
                    time.sleep(1)
            
            except:
                print('error')
            i=i+1