#한지성, 김윤태
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

for page in range(1,6):
 url = "https://book.naver.com/bestsell/bestseller_list.nhn?cp=yes24&cate=total&bestWeek=2021-05-2&indexCount=&type=list&page="+ str(page)

 driver = webdriver.Chrome(ChromeDriverManager().install())
 driver.implicitly_wait(30)


 # 네이버의 베스트셀러 웹페이지를 가져옵니다.
 driver.get(url)
 bsObject = BeautifulSoup(driver.page_source, 'html.parser')



 # 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
 book_page_urls = []
 for index in range(0, 25):
    dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
    link = dl_data.select('a')[0].get('href')
    book_page_urls.append(link)



 # 메타 정보와 본문에서 필요한 정보를 추출합니다.
 for index, book_page_url in enumerate(book_page_urls):

    driver.get(book_page_url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')

    title = bsObject.find('meta', {'property':'og:title'}).get('content')
    author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
    plot = bsObject.find('meta', {'property':'og:description'}).get('content')
   

    print(title,"/", author,'\n',plot )