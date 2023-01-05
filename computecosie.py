from sklearn.feature_extraction.text import CountVectorizer
import numpy as np 
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import lda

def computecosine(df, ct, name):
    df1 = pd.DataFrame(columns=['Paper_ID', 'Title', 'Abstract'])
    if(len(ct) < 2 ):
        return
    for i in range(0, len(df)):
        if df.Paper_ID[i] in ct:
             df1 = df1.append({'Paper_ID':df.Paper_ID[i] , 'Title':df.Title[i], 'Abstract': df.Abstract[i]   }, ignore_index=True)
    
    vectorizer = CountVectorizer() #tokenizer = lda.spacy_tokenizer
    data_vectorized = vectorizer.fit_transform(df1.Abstract)
    matrix= cosine_similarity(data_vectorized, data_vectorized)
    matrix = np.asarray(matrix)
    avg = matrix.mean()
    #print("\t>>the mean score of community detected by ",name ,"with lenght",len(ct)," : ",avg )
    return avg
