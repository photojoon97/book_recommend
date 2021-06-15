#데이터셋에 score 컬럼 추가

import pandas as pd

data = pd.read_csv('./extract_data.csv', low_memory=False)
data['content'] = data['content'].fillna('')

def grade_weight(data):
    #개별 영화 평점
    #
    # v : 개별 영화 투표 수
    # m : 최소 투표 횟수
    # r : 개별 영화 평균 평점
    # c : 전체 영화 평균 평점
    # 가중평점 공식: (v/(v+m)) r + (m/(v+m)) * c

    v = data['review']
   
    r = data['grade']
    return ((v/(v+m)) * r) + ((m/(v+m)) * c)

c = data['grade'].mean()
print('c : ', c)
#최소 투표 횟수
m = data['review'].quantile(0.90)
print('m : ', m)
data['score'] = data.apply(grade_weight, axis=1) #가중 평점을 추가

print(data.head(10))

data.drop(['Unnamed: 0'], axis = 1, inplace = True) #Unnamed: 0 열 제거

data.to_csv('./extract_data_add_score.csv', sep=',', na_rep='NaN')

