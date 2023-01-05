import scispacy
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from tqdm import tqdm
import numpy as np 
import pandas as pd 
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity
import tfIDF
from collections import Counter 

nlp = spacy.load("en_core_sci_sm")


def spacy_tokenizer(sentence):
    return [word.lemma_ for word in nlp(sentence) if not (word.like_num or word.is_stop or word.is_punct or word.is_space or len(word)==1)]

def print_top_words(model, vectorizer, n_top_words):
    feature_names = vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        message = "\nTopic #%d: " % topic_idx
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

def LDA (dataFrame):
    print(">>LDA partitioning process")
    vectorizer = CountVectorizer(tokenizer = spacy_tokenizer)
    data_vectorized = vectorizer.fit_transform(tqdm(dataFrame.Abstract))
    #print("LDA count vectroizer shape" ,data_vectorized.shape)
    
    lda = LatentDirichletAllocation(n_components=20, random_state=0)
    lda.fit(data_vectorized)
    
    X= lda.transform(data_vectorized)
    #print(X.shape)
    k = 20
    kmeans = KMeans(n_clusters=k, random_state=42).fit(X)
    clusters = kmeans.predict(X)
    print(">> CLusters for LDA are as following")
    dataFrame['ClusterIndex'] = clusters     
    con = Counter(dataFrame.ClusterIndex)
    print (con) 
    return tfIDF.papersIncluster(dataFrame)
    
