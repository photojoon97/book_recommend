#2018038092 안준

from numpy.core.fromnumeric import shape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse #TF-IDF matrix를 내보내기 위함
from konlpy.tag import Okt
import time

#영화 추천
def recommend(title, cosine_sim):
    print('indices\'s type : ',type(indices)) 
    idx = indices[title] 
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1],reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]

start = time.time() #실행시간 측정

data = pd.read_csv('./movie_dataset.csv', low_memory=False)
data['content'] = data['content'].fillna('')#fillna() 결측치 대체함수, dropna() 함수로 결측치 제거 시 index is out of bound 발생하기 때문
#data = data['content'].dropna() #none값이 있는 행 제거, 결측값이 있으면 okt 형태소 분석 단계에서 오류 발생


#텍스트 데이터 전처리 ,명사만 추출 (추후 동사 추출과 불용어 제거)
okt = Okt()
for i in data.index:
    result = okt.nouns(data.at[i,'content'])
    data.at[i,'content'] = result #i번째 행 content열에 전처리 결과 대입
    data.at[i,'content'] = ' '.join(data.at[i, 'content']) #list는 토큰화할 수 없기 때문에 문자열로 변환
    #print(data.at[i,'content'])

#토큰화
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(data['content']) #줄거리를 기반으로 ~
print(tfidf_matrix.shape)
print('TF-IDF Type : ', type(tfidf_matrix)) #matrix 타입 확인

#매트릭스 내보내기
scipy.sparse.save_npz('./tf-idf_matrix.npz',tfidf_matrix) #백터화 이후 재실행 시 실행시간 단축을 위해 ~

#매트릭스 불러오기
#tfidf_matrix = scipy.sparse.load_npz('path of matrix')

#코사인 유사도
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(data.index, index=data['title']).drop_duplicates()
print("실행시간 : ",time.time() - start)

#영화제목 입력
while True:
    title = input('영화 제목을 입력하세요 : ')
    if (data['title'] == title).any(): #dataframe에 사용자가 입력한 제목이 있는지 검색
        print(recommend(title, cosine_sim))
        break
    else:
        continue


