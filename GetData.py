"""
--------------------------------------
Created on Fri May 21 02:18:38 2021

@author: SooYeon Yim(team7, UFO/2020039017)

Description:a web crawler that scraps book titles and introduction(abstract) data from Naver Book Home

Name:GetData
--------------------------------------
"""


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url=r"https://book.naver.com/category/index.nhn?cate_code=100010010"

driver=webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)

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


    

