# -*- coding: utf-8 -*-
import re, numpy, scipy.io
import pandas as pd



TRAIN = pd.read_csv('/Users/qianwang/study/NEU/hack the lab/data_v1.1/training_raw_data.csv')

TEST = pd.read_csv('/Users/qianwang/study/NEU/hack the lab/data_v1.1/Youtube05-Shakira.csv')

NUM_OF_FEATURES = 30

FIND_AND_REPLACE = {
    "<[^<>]+>" : " ",
    "[0-9]+" : "number",
    "(http|https)://[^\s]*" : "httpaddr",
    "[^\s]+@[^\s]+" : "emailaddr",
    "[$]+" : "dollar"}



'''
GIVEN: a comment(string)
RETURNS: a normalized comment(string)
'''
def NormalizeComment(s,find_replace = FIND_AND_REPLACE):
    s = s.lower()
    for key in find_replace:
        s = re.sub(key, find_replace[key], s)
    return s


'''
GIVEN: a dataframe
RETURN: an updated datafram with a new column named NORM_CONTENT
        containing normalized comments
'''
def normalizeDF(df):
    df['NORM_CONTENT'] = df['CONTENT'].apply(NormalizeComment)


 
'''
GIVEN: a list of words(strings)
RETURNS: a dictionary, where key is a word and value is word frequence.
'''            
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


'''
GIVEN:  a dictionary of words and corresponding frequencies, the number of 
        frenquent words need to be used as features
RETURNS: a list of words arranged from hignes frequency to lowest.
'''                
def wordRank(wordDic, n):
    wordObjList = []
    wordRankList = []
    for word in wordDic:
        wordobj = Wordobj(word, wordDic[word])
        wordObjList.append(wordobj)
        wordObjList.sort(key=lambda x: x.count, reverse=True)
    for wordObj in wordObjList:
        wordRankList.append(wordObj.word)  
    return wordRankList[0:n]

    
        
'''
GIVEN: a dataframe and the number of features
RETURNS: a list of highest frequent words as features
'''               
def getFeatures(df, n):
    allComments = ""
    for s in df['NORM_CONTENT']:
        allComments += s       
    wordDic = wordfrequence(s.split())
    return wordRank(wordDic, n)
      


'''
GIVEN: a comment(string), features(a list of words) and whether the comment is spam
RETURNS: a list of floats represent whether the feature words exist in the comment
'''  
def commentToData(s, features,spam):
    result = {}
    for word in features:
        if word in s:
            result[word] = 1
        else:
            result[word] = 0
    data = []
    for key in result:
        data.append(float(result[key]))
    data.append(float(spam))
    return data



'''
GIVEN: nomalized dataframe and features
RETURNS: a matrix(list of list of numbers representing whether a feature word
         is in a comment
'''
def normalizedDFToDataMatrix(df, features):
    matrix = []
    for i in range(len(df['CONTENT'])):
        data = commentToData(df['CONTENT'][i],features,df['CLASS'][i])
        matrix.append(data)
    return matrix
    



def main():
    normalizeDF(TRAIN)
    normalizeDF(TEST)
    spam = TRAIN[TRAIN['CLASS'] == 1]
    features = getFeatures(spam, NUM_OF_FEATURES)
    testMatrix = normalizedDFToDataMatrix(TRAIN, features)
    trainMatrix = normalizedDFToDataMatrix(TEST, features)
    scipy.io.savemat('/Users/qianwang/study/NEU/hack the lab/data_v1.1/test.mat', mdict={'test':testMatrix })
    scipy.io.savemat('/Users/qianwang/study/NEU/hack the lab/data_v1.1/train.mat', mdict={'train': trainMatrix})
    print features          

if __name__ == "__main__":
    main()