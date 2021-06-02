<<<<<<< HEAD
=======

>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640
"""
--------------------------------------
@author: Joon Ahn(team7, UFO/2018038092)
Description: Book recommendation system using cosine similarity
<<<<<<< HEAD
Name:recommend.py
=======
Name:recommendation.py
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640
--------------------------------------
"""

from numpy.core.fromnumeric import shape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse #TF-IDF matrix를 내보내기 위함
from konlpy.tag import Okt
<<<<<<< HEAD
from eunjeon import Mecab 
import string
import time
import csv


def search_title(data):
    #2018038092 안준

    while True:
        while True:
            input_title = input("\n\n제목을 입력하세요  : ")
            titles = data[data['title'].str.contains(input_title)] #부분일치하는 문자열 행을 모두 찾음
            if titles.empty:
                continue
            else:
                print("\n\n",titles['title'], end="\n\n")
                break
        
        title_num = int(input("제목 번호를 입력하세요 (재검색 -1): "))
        if title_num == -1:
            continue
        else:
            return title_num

def add_weight():
    #추가 예정
    print(' ')

#영화 추천
def recommend_book(title, cosine_sim):
    print("\nrecommending book...\n")
    
    idx = title
    sim_scores = list(enumerate(cosine_sim[idx]))
    
=======
import time
import csv

#영화 추천
def recommend_book(title, cosine_sim, indices):
    print('indices\'s type : ',type(indices)) 
    idx = indices[title] 
    print(idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640
    sim_scores = sorted(sim_scores, key=lambda x: x[1],reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]

def preprocessing(data):
<<<<<<< HEAD
    #2018038092 안준

    print("\ndata preprocessing...\n")
=======
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640
    #텍스트 데이터 전처리 ,명사만 추출 (추후 동사 추출과 불용어 제거)
    okt = Okt()

    #불용어 처리 단어 불러오기
    temp = []
    f = open('stopwords.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    stopwords = sum(temp, []) #2차원 리스트를 1차원 리스트로 변환
    f.close()

    for i in data.index:
        word_token = okt.pos(data.at[i,'content'], norm=True, stem=True)
        filtering = [x for x,y in word_token if y in ['Noun', 'Adjective', 'Verb']] # 명사, 형용사, 동사만 추출

        #공백 제거
<<<<<<< HEAD
=======
        #filtering = [x.strip() for x in filtering]
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640
        new_filtering = [i.replace(' ', '') for i in filtering]

        #불용어 처리
        result = []
        for word in new_filtering:
            if word not in stopwords: #stopwords.csv 파일에서 불러옴.
<<<<<<< HEAD
=======
                #print(stopwords)
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640
                result.append(word)
    
        #dataframe에 추가
        data.at[i,'content'] = result #i번째 행 content열에 전처리 결과 대입
<<<<<<< HEAD
        data.at[i,'content'] = ' '.join(data.at[i, 'content']) #list는 토큰화할 수 없기 때문에 하나의 문자열로 결합
    return data

def cosine(data):
    print("\nCalculating cosine similarity\n")
    
    ##토큰화
    #tfidf = TfidfVectorizer()
    #tfidf_matrix = tfidf.fit_transform(data['content']) #줄거리를 기반으로 ~
    #print(tfidf_matrix.shape)
    #print('TF-IDF Type : ', type(tfidf_matrix)) #matrix 타입 확인

    #매트릭스 내보내기
    #scipy.sparse.save_npz('./tf-idf_matrix.npz',tfidf_matrix) #백터화 이후 재실행 시 실행시간 단축을 위해 ~

    #매트릭스 불러오기
    tfidf_matrix = scipy.sparse.load_npz('./tf-idf_matrix.npz')

    #코사인 유사도
    #cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print("\ncosine_sim's type : ",type(cosine_sim), end='\n')
    print("\ncosine sim : \n", cosine_sim, end='\n\n')

    return cosine_sim
=======
        #print(result, end="\n\n")
        data.at[i,'content'] = ' '.join(data.at[i, 'content']) #list는 토큰화할 수 없기 때문에 하나의 문자열로 결합
        #print(data.at[i,'content'])
    return data

def cosine(data):
    #토큰화
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(data['content']) #줄거리를 기반으로 ~
    print(tfidf_matrix.shape)
    print('TF-IDF Type : ', type(tfidf_matrix)) #matrix 타입 확인

    #매트릭스 내보내기
    scipy.sparse.save_npz('./tf-idf_matrix(test).npz',tfidf_matrix) #백터화 이후 재실행 시 실행시간 단축을 위해 ~

    #매트릭스 불러오기
    #tfidf_matrix = scipy.sparse.load_npz('path of matrix')

    #코사인 유사도
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(data.index, index=data['title']).drop_duplicates()

    return cosine_sim, indices
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640


###############################

start = time.time() #실행시간 측정

<<<<<<< HEAD
data = pd.read_csv('./extract_data.csv', low_memory=False)
data = data.dropna(axis=0) #결측치 행 제거
data['title'] = data['title'].fillna('')#fillna() 결측치 대체함수, dropna() 함수로 결측치 제거 시 index is out of bound 발생하기 때문
data['content'] = data['content'].fillna('')


#data = preprocessing(data)

cosine_sim = cosine(data)
=======
data = pd.read_csv('./test.csv', low_memory=False)
data['content'] = data['content'].fillna('')#fillna() 결측치 대체함수, dropna() 함수로 결측치 제거 시 index is out of bound 발생하기 때문
#data = data['content'].dropna() #none값이 있는 행 제거, 결측값이 있으면 okt 형태소 분석 단계에서 오류 발생

data = preprocessing(data)

cosine_sim, indices = cosine(data)
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640

print("실행시간 : ",time.time() - start)

recommended_book_list = []

<<<<<<< HEAD
while True:
    title = search_title(data)
    recommended_book_list = recommend_book(title, cosine_sim) #제목의 정확한 인덱스 값을 주지 않으면 ValueError 발생
    print(recommended_book_list)
    
    if input('재검색? (-1) : ') == '-1':
        continue
    else:
        break
    
=======
#영화제목 입력
while True:
    title = input('도서 제목을 입력하세요 : ')
    if (data['title'] == title).any(): #dataframe에 사용자가 입력한 제목이 있는지 검색
        recommended_book_list = recommend_book(title, cosine_sim, indices)
        print(recommended_book_list)
        break
    else:
        continue
>>>>>>> 8ae0580bb601ae2f86927f08161a5da5706a0640


