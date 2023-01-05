from sklearn.feature_extraction.text import CountVectorizer
import numpy as np 
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import lda
# taken from https://stackoverflow.com/questions/29484529/cosine-similarity-between-two-words-in-a-list
def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

def computeInterCosine(ls1, ls2,datasetdict):
    allpaperssimlarity = []
    for paper in ls1:
        for papers in ls2:
            cosdist = []
            for word in datasetdict[paper]:
                for words in datasetdict[papers]:
                    cosdist.append(cosdis(word2vec(word), word2vec(words)))
            avg = sum(cosdist) / len(cosdist)         
            #print("the cosine distance between the two papers is ", avg)
            allpaperssimlarity.append(avg)
    tavg = sum(allpaperssimlarity) / len(cosdis)
    return tavg



            





