"""
--------------------------------------
Created on Fri May 29 2021
@author: Joon Ahn(team7, UFO/2018038092)
Description: The csv file that extracted only Korean and English numbers from crawlingdata.csv file
Name:extract.py
--------------------------------------
"""
import re
import pandas as pd

patt = '[^A-Za-z0-9가-힣]' #영어, 숫자, 한글 추출 정규식 패턴
data = pd.read_csv('./crawlingdata.csv', low_memory=False)
data['content'] = data['content'].fillna('')
cnt = 0
print(data.head())

print('\n\n진행사항 : ', end='')

for i in data.index:
    title = ''
    content = ''

    title = data.at[i, 'title']
    content = data.at[i, 'content']

    title = re.sub(pattern=patt, repl=' ', string=title)
    content = re.sub(pattern=patt, repl=' ', string=content)

    data.at[i, 'title'] = title
    data.at[i, 'content'] = content 
    
    cnt += 1
    if cnt == 190:
        cnt = 0
        print('#', end='')
    
    #print('\ntitle : ', data.at[i, 'title'])
    #print('\n\ncontent : ',data.at[i, 'content'])

data.to_csv('./extract_data.csv', sep=',', na_rep='NaN')

