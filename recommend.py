from numpy.core.fromnumeric import shape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse #TF-IDF matrix를 내보내기 위함
from konlpy.tag import Mecab
import time
import csv

class recommend:

    def __init__(self, data_link,stopwords_link) -> None:
        self.data = pd.read_csv(data_link, index_col = 0)
        self.data = self.data.dropna(axis=0) #결측치 행 제거
        self.data['title'] = self.data['title'].fillna('')#fillna() 결측치 대체함수, dropna() 함수로 결측치 제거 시 index is out of bound 발생하기 때문
        self.data['content'] = self.data['content'].fillna('')
        self.data = self.data.drop_duplicates(['title'], ignore_index = True) #중복되는 제목 제거
        #형변환 (가중 평점을 계산하기 위해 데이터프레임의 값을 숫자형으로 변환해야 함)
        self.data['grade'] = pd.to_numeric(self.data['grade'])
        self.data['review'] = pd.to_numeric(self.data['review'])
        ###가중평점 추가####
        #전체 영화 평균 평점
        self.c = self.data['grade'].mean()
        print('\n전체 영화 평균 평점 : %.5f'%self.c)
        #최소 투표 횟수
        self.m = self.data['review'].quantile(0.90)
        print('최소 투표 횟수 : ', self.m)

        self.f = open(stopwords_link, 'r', encoding='utf-8')
    
    def add_weight(self):
        m = self.m
        c = self.c
        v = self.data['review']
        r = self.data['grade']

        return (v / (v+m)) * r + (m / (v+m)) * c

    def search_title(self) -> int:
        title_num = None
        input_title = input("\n\n제목을 입력하세요  : ")
        titles = self.data[self.data['title'].str.contains(input_title)] #부분일치하는 문자열 행을 모두 찾음
        if titles.empty:
            return 0
        else:
            print("\n검색한 제목 : ",titles['title'], end="\n\n")
            title_num = int(input("제목 번호를 입력하세요 (재검색 -1): "))
        return title_num
                
    
    def preprocessing(self):
        print("\ndata preprocessing...\n")
        mecab = Mecab()
        #불용어 처리 단어 불러오기
        temp = []
        
        reader = csv.reader(self.f)
        for row in reader:
            temp.append(row)
        stopwords = sum(temp, []) #2차원 리스트를 1차원 리스트로 변환
        self.f.close()

        for i in self.data.index:
            word_token = mecab.pos(self.data.at[i,'content'])
            filtering = [x for x,y in word_token if y in ['NNG', 'NNP', 'VV', 'VA' ]]  #일반명사, 고유명사, 동사, 형용사

            #공백 제거
            new_filtering = [i.replace(' ', '') for i in filtering]

            #불용어 처리
            result = []
            for word in new_filtering:
                if word not in stopwords: #stopwords.csv 파일에서 불러옴.
                    result.append(word)

            #dataframe에 추가
            self.data.at[i,'content'] = result #i번째 행 content열에 전처리 결과 대입
            self.data.at[i,'content'] = ' '.join(self.data.at[i, 'content']) #list는 토큰화할 수 없기 때문에 하나의 문자열로 결합

        print('\ncomplete data preprocessing.')
    
    def calc_cosine_sim(self):
        print("\nCalculating cosine similarity\n")
    
        ##토큰화
        #tfidf = TfidfVectorizer()
        #tfidf_matrix = tfidf.fit_transform(self.data['content']) #줄거리를 기반
        #print(tfidf_matrix.shape)
        #print('TF-IDF Type : ', type(tfidf_matrix)) #matrix 타입 확인

        #매트릭스 내보내기
        #scipy.sparse.save_npz('./tf-idf_matrix.npz',tfidf_matrix) #백터화 이후 재실행 시 실행시간 단축을 위해 ~

        #매트릭스 불러오기
        tfidf_matrix = scipy.sparse.load_npz('./tf-idf_matrix.npz')

        #코사인 유사도
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        print("\ncosine_sim's type : ",type(self.cosine_sim), end='\n')
    
    def recommend_book(self, title_num):
        print("\nrecommending book...")
        print('\ntype : ',type(title_num))

        tempDf = pd.DataFrame() #빈 데이터프레임 생성

        idx = title_num
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1],reverse=True)
        sim_scores = sim_scores[1:50] #유사한 도서 50개 추출

        movie_indices = [i[0] for i in sim_scores] #유사한 순서의 인덱스 리스트

        for i in movie_indices:
            #movie_indices의 인덱스를 가지고 행을 추출하여 새로운 데이터프레임에 추가
            temp =  dict(self.data.iloc[i])
            tempDf = tempDf.append(temp,ignore_index=True)
        tempDf = tempDf.sort_values('score',ascending=False)[:10] #score를 기준으로 데이터프레임 정렬
        return tempDf

    def search(self):
        start = time.time() #실행시간 측정
        
        #self.data['score'] = self.data.apply(self.add_weight(), axis=1) # data에 가중 평점 열을 추가
        self.data.drop(self.data.loc[self.data['score'] < self.c].index, inplace=True) #전체 영화 평균평점보다 낮은 영화 제거
        #################
        #self.preprocessing()
        self.calc_cosine_sim()

        recommend_book_list = []
        print("실행시간 : ",time.time() - start)

        while True:
            select = self.search_title()
            print('\ntitle num : ',select)
            recommend_book_list = self.recommend_book(select)
            print(recommend_book_list[['title', 'score']])
            
            if input('재검색? (-1) : ') == '-1':
                continue
            else:
                break


test = recommend('./extract_data_add_score.csv','stopwords.csv')
test.search()


