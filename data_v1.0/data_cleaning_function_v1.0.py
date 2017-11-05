import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import re
import numpy, scipy.io



df1 = pd.read_csv('/Users/qianwang/study/NEU/hack the lab/data_v1.0/total.csv')
# df3 = pd.read_csv('/Users/qianwang/study/NEU/hack the lab/raw data/Youtube03-LMFAO.csv')
# df4 = pd.read_csv('/Users/qianwang/study/NEU/hack the lab/raw data/YYoutube04-Eminem.csv')
df5 = pd.read_csv('/Users/qianwang/study/NEU/hack the lab/data_v1.0/Youtube05-Shakira.csv')


content = df1['CONTENT'][df1['CLASS'] == 1]
comments =[]
for e in content:
    comments.append(e)


for i in range(len(comments)):
    comments[i] = comments[i].lower()
    comments[i] = re.sub("<[^<>]+>", " ",comments[i])
    comments[i] = re.sub("[0-9]+" ,"number", comments[i])
    comments[i] = re.sub('(http|https)://[^\s]*', 'httpaddr', comments[i])
    comments[i] = re.sub('[^\s]+@[^\s]+', 'emailaddr', comments[i])
    comments[i] = re.sub('[$]+', 'dollar', comments[i])
    
def wordfrequence (wordList):
    result = {}
    for w in wordList:
        if w not in result:
            result[w] = 1
        else: result[w] +=1
    return result
    
    
class Wordobj:
    def __init__(self, word, count):
        self.word = word
        self.count = count

                
def wordRank(wordDic):
    wordObjList = []
    wordRankList = []
    for word in wordDic:
        wordobj = Wordobj(word, wordDic[word])
        wordObjList.append(wordobj)
        wordObjList.sort(key=lambda x: x.count, reverse=True)
    for wordObj in wordObjList:
        wordRankList.append(wordObj.word)  
    return wordObjList, wordRankList
    

def stringToLow(s):
    s = s.lower()
    s = re.sub("<[^<>]+>", " ",s)
    s = re.sub("[0-9]+" ,"number", s)
    s = re.sub('(http|https)://[^\s]*', 'httpaddr', s)
    s = re.sub('[^\s]+@[^\s]+', 'emailaddr', s)
    s = re.sub('[$]+', 'dollar', s)
    return s.split()
  
def commentToData(s, features,spam):
    comment = stringToLow(s)
    result = {}
    for word in features:
        if word in comment:
            result[word] = 1
        else:
            result[word] = 0
    l = []
    for key in result:
        l.append(float(result[key]))
    l.append(float(spam))
    return l
    
low = []
for s in comments:   
    for w in s.split():
        low.append(w)

wordDic = wordfrequence(low)
wordObjList, wordRankList = wordRank(wordDic)
features = wordRankList[0:30]


matrix = []
for i in range(370):
    data = commentToData(df5['CONTENT'][i],features,df5['CLASS'][i])
    matrix.append(data)


          
# wordList1 = ['a', 'a', 'b', 'b', 'b','c']    
# wordDic1 = wordfrequence (wordList1)
# 
# wordObjList1, wordRankList1 = wordRank(wordDic1)
# print wordRankList1
# for wordObj in wordObjList1:
#     print wordObj.word, wordObj.count
#     
#     
# print commentToData(['a', 'c','d','e'], ['a','c', 'f'])

# newdf = pd.DataFrae(columns = features)
# 
# for i in range(350):
#     newdf.iloc[i] =

# scipy.io.savemat('/Users/qianwang/study/NEU/hack the lab/raw data/test.mat', mdict={'train': matrix})