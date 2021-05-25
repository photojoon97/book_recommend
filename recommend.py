
"""
--------------------------------------
Created on Fri May 25 2021
@author: Joon Ahn(team7, UFO/2018038092)
Description: Book recommendation system using cosine similarity
Name:recommendation.py
--------------------------------------
"""

from numpy.core.fromnumeric import shape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse #TF-IDF matrix를 내보내기 위함
from konlpy.tag import Okt
import time
import csv

#영화 추천
def recommend_book(title, cosine_sim, indices):
    print('indices\'s type : ',type(indices)) 
    idx = indices[title] 
    print(idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1],reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]

def preprocessing(data):
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
        #filtering = [x.strip() for x in filtering]
        new_filtering = [i.replace(' ', '') for i in filtering]

        #불용어 처리
        result = []
        for word in new_filtering:
            if word not in stopwords: #stopwords.csv 파일에서 불러옴.
                #print(stopwords)
                result.append(word)
    
        #dataframe에 추가
        data.at[i,'content'] = result #i번째 행 content열에 전처리 결과 대입
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


###############################

start = time.time() #실행시간 측정

data = pd.read_csv('./test.csv', low_memory=False)
data['content'] = data['content'].fillna('')#fillna() 결측치 대체함수, dropna() 함수로 결측치 제거 시 index is out of bound 발생하기 때문
#data = data['content'].dropna() #none값이 있는 행 제거, 결측값이 있으면 okt 형태소 분석 단계에서 오류 발생

data = preprocessing(data)

cosine_sim, indices = cosine(data)

print("실행시간 : ",time.time() - start)

recommended_book_list = []

#영화제목 입력
while True:
    title = input('도서 제목을 입력하세요 : ')
    if (data['title'] == title).any(): #dataframe에 사용자가 입력한 제목이 있는지 검색
        recommended_book_list = recommend_book(title, cosine_sim, indices)
        print(recommended_book_list)
        break
    else:
        continue


