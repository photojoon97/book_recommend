"""
--------------------------------------
@author: Joon Ahn(team7, UFO/2018038092)
Description: Book recommendation system using cosine similarity
Name:recommend.py
--------------------------------------
"""

from numpy.core.fromnumeric import shape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse #TF-IDF matrix를 내보내기 위함
from konlpy.tag import Mecab
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
            print('\n선택한 제목 : ',data.at[title_num,'title'])
            return title_num

#영화 추천
def recommend_book(title, cosine_sim):
    #2018038092 안준
    print("\nrecommending book...\n")

    tempDf = pd.DataFrame() #빈 데이터프레임 생성

    idx = title
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1],reverse=True)
    sim_scores = sim_scores[1:50] #유사한 도서 50개 추출

    movie_indices = [i[0] for i in sim_scores] #유사한 순서의 인덱스 리스트

    #print(movie_indices[:20]) #유사한 도서의 인덱스 순서

    for i in movie_indices:
        #movie_indices의 인덱스를 가지고 행을 추출하여 새로운 데이터프레임에 추가
        temp =  dict(data.iloc[i])
        tempDf = tempDf.append(temp,ignore_index=True)
    tempDf = tempDf.sort_values('score',ascending=False)[:10] #score를 기준으로 데이터프레임 정렬
    
    return tempDf

def preprocessing(data):
    #2018038092 안준
    #텍스트 데이터 전처리 ,명사만 추출 (추후 동사 추출과 불용어 제거)

    print("\ndata preprocessing...\n")
    
    mecab = Mecab()
    
    #불용어 처리 단어 불러오기
    temp = []
    f = open('stopwords.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    for row in reader:
        temp.append(row)
    stopwords = sum(temp, []) #2차원 리스트를 1차원 리스트로 변환
    f.close()

    for i in data.index:
        word_token = mecab.pos(data.at[i,'content'])
        filtering = [x for x,y in word_token if y in ['NNG', 'NNP', 'VV', 'VA' ]]  #일반명사, 고유명사, 동사, 형용사

        #공백 제거
        new_filtering = [i.replace(' ', '') for i in filtering]

        #불용어 처리
        result = []
        for word in new_filtering:
            if word not in stopwords: #stopwords.csv 파일에서 불러옴.
                result.append(word)
    
        #dataframe에 추가
        data.at[i,'content'] = result #i번째 행 content열에 전처리 결과 대입
        data.at[i,'content'] = ' '.join(data.at[i, 'content']) #list는 토큰화할 수 없기 때문에 하나의 문자열로 결합
    return data

def calc_cosine_sim(data):
    print("\nCalculating cosine similarity\n")
    
    ##토큰화
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(data['content']) #줄거리를 기반
    print(tfidf_matrix.shape)
    print('TF-IDF Type : ', type(tfidf_matrix)) #matrix 타입 확인
    
    #매트릭스 내보내기
    scipy.sparse.save_npz('./tf-idf_matrix.npz',tfidf_matrix) #백터화 이후 재실행 시 실행시간 단축을 위해 ~

    #매트릭스 불러오기
    #tfidf_matrix = scipy.sparse.load_npz('./tf-idf_matrix.npz')

    #코사인 유사도
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print("\ncosine_sim's type : ",type(cosine_sim), end='\n')

    return cosine_sim

def add_weight(data):
    #개별 영화 평점
    #
    # v : 개별 영화 투표 수
    # m : 최소 투표 횟수
    # r : 개별 영화 평균 평점
    # c : 전체 영화 평균 평점
    # 가중평점 공식: (v/(v+m)) r + (m/(v+m)) * c
    #https://www.datacamp.com/community/tutorials/recommender-systems-python
    
    v = data['review'] 
    
    r = data['grade'] 

    return (v / (v+m)) * r + (m / (v+m)) * c


start = time.time() #실행시간 측정

data = pd.read_csv('./extract_data_add_score.csv', index_col = 0)
data = data.dropna(axis=0) #결측치 행 제거
data['title'] = data['title'].fillna('')#fillna() 결측치 대체함수, dropna() 함수로 결측치 제거 시 index is out of bound 발생하기 때문
data['content'] = data['content'].fillna('')
data = data.drop_duplicates(['title'], ignore_index = True) #중복되는 제목 제거

#형변환 (가중 평점을 계산하기 위해 데이터프레임의 값을 숫자형으로 변환해야 함)
data['grade'] = pd.to_numeric(data['grade'])
data['review'] = pd.to_numeric(data['review'])

###가중평점 추가####
#전체 영화 평균 평점
c = data['grade'].mean()
print('\n전체 영화 평균 평점 : %.5f'%c)
#최소 투표 횟수
m = data['review'].quantile(0.90)
print('최소 투표 횟수 : ', m)


data['score'] = data.apply(add_weight, axis=1) # data에 가중 평점 열을 추가
data.drop(data.loc[data['score'] < c].index, inplace=True) #전체 영화 평균평점보다 낮은 영화 제거
#################

data = preprocessing(data) #데이터 전처리

cosine_sim = calc_cosine_sim(data) #코사인 유사도 계산

recommended_book_list = []

while True:
    title = search_title(data)
    recommended_book_list = recommend_book(title, cosine_sim) #제목의 정확한 인덱스 값을 주지 않으면 ValueError 발생
    print(recommended_book_list[['title', 'score']])
    
    if input('재검색? (-1) : ') == '-1':
        continue
    else:
        break
    


