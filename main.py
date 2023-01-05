#importing classes that i made for the work
from Readdata import readdata
import BasicChanges
import topwords
import graph
import papernames
import Presentation
import computecosie
import tfIDF
import lda
import Goodness
import intercosineSimilarity

#importing some usefull libraries
import pandas as pd
import collections
from tqdm import tqdm

# Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

#selective words for paper selection
filterpaperList = ["covid","covid-19","sars-cov-2","sars", "cov3", "ncov", "coronavirus", "novel","sars-cov"]

#reading dataset and converting it into dataframe by applying filters on the dataset.
name = "metadata.csv"
data = readdata(name,filterpaperList,"TF")
mainDataFrame = data.getDF()
print(mainDataFrame.head())

ctTf = tfIDF.tf(mainDataFrame)      #using TF_IDF for making clusters of documents 
ctLda  = lda.LDA(mainDataFrame)     #using LDA to find clusters of documents

#getting required data for making bipartite network
datasetdict =  data.getdatsetDict()
nodewords = data.getWordpaper()
nodePaper = data.getNodepaper()
allwordsDic = data.getAlldatsetDict()

BasicChanges.showingDataValues(data)        #showing basic results related to dataset

#Removel of frequent words as they are occuring in most of the papers
toptenwords = BasicChanges.topwordsCount(datasetdict)
for wordd in filterpaperList:
    if wordd in toptenwords:
        continue
    else:
        toptenwords.append(wordd)
nodewords = BasicChanges.removewords(toptenwords,nodewords)
datasetdict = BasicChanges.removedatasetdict(toptenwords,datasetdict)

#calling to make bipartie graph and return a weighted projection of that bipartite graph
G = graph.createBgraph(nodePaper,nodewords,datasetdict,False)

ctBp =graph.patterns(G,datasetdict)             #best partition community detection algorithm
ctGa = graph.greedyApproch(G,datasetdict)       #greedy approch community detection algorithm


#Goodness.metrics(ctBp,G)
#Goodness.metrics(ctGa,G)

#Result dataFrame of each community for every algorithm
df1 = pd.DataFrame(columns=['algorithm','communitynumber' ,'topwords', 'numberofpapers'])
df1 = topwords.countTopwords(ctBp, datasetdict, df1, 'ctBp')
df1 = topwords.countTopwords(ctTf, datasetdict, df1, 'ctTf')
df1 = topwords.countTopwords(ctLda, datasetdict, df1, 'ctLda')
df1 = topwords.countTopwords(ctGa, datasetdict, df1, 'ctGa')

#preparing presenations for each approach
def ResultsPresentation(comunities, datasetdict,name):
    comLis = graph.topWordsCount(comunities,datasetdict)
    Presentation.wordMap(comLis,name)                   #wordmap
    comparison=graph.comparisonOfcommunites(comLis)
    Presentation.compplot(comparison,name)              #comaprison with others
    Presentation.worddisp(comLis,name)                  #top occuring words list

ResultsPresentation(ctBp,datasetdict,"ctBp")    #Presentations for best partitions
ResultsPresentation(ctTf,datasetdict,"ctTf")    #Presentations for TF-IDF partitions
ResultsPresentation(ctLda,datasetdict,"ctLda")  #Presenations for LDA partitions
ResultsPresentation(ctGa,datasetdict,"ctGa")    #Presenattion for Greedy approch paritions

#computeing intra community clusters cosine similarity score
simLis = []
def computingCosineSimilarity(ct, name):
    sum = 0.0
    count = 0
    for communityy in ct:
        avg = computecosie.computecosine(mainDataFrame, ct[communityy],name)
        if(avg is None):
            continue
        avg = float(avg)
        simLis.append(avg)
        sum= avg + sum
        count+=1
    print("\t>>The Intra cosine similarity of ",name," approach is = ", sum/count)


def makingstr(ls):
    str = ""
    for word in ls:
        str+=word+" "
    return str

#bp
interSumLis = []
def intercosine(ct):
    lis = []
    for com in tqdm(ct):
        if(len(ct[com]) < 2):
            continue
        avgList = []
        for paper in ct[com]:
            ls = []
            ls.append(allwordsDic[paper])
            for com1 in ct:
                if(len(ct[com]) < 2):
                    continue
                if com == com1:
                    continue
                else:
                    for papers in ct[com1]:
                        ls.append(allwordsDic[papers])
            count_vectorizer = CountVectorizer()
            sparse_matrix = count_vectorizer.fit_transform(ls)
            matrix=cosine_similarity(sparse_matrix[0:1], sparse_matrix)
            #print(matrix)
            matrix = np.asarray(matrix)
            avg = matrix.mean()
            avgList.append(avg)
        comavg = sum(avgList)/len(avgList)
        lis.append(comavg)
        interSumLis.append(comavg)
        #print("the average inter cosine similiarty of the {} is {}".format(com,comavg))
    BpAvg= sum(lis)/ len(lis)
    return BpAvg

vectorizer = CountVectorizer() #tokenizer = lda.spacy_tokenizer
data_vectorized = vectorizer.fit_transform(mainDataFrame.Abstract)   
matrix= cosine_similarity(data_vectorized, data_vectorized)
matrix=np.asarray(matrix)
print(">> the average cosine similairty of all papers before clustering = ", matrix.mean())

print("\n>>inter similarity scores for each community using Best Partition approach")
print("\t>>the average inter cosine similarity of BP is {}".format(intercosine(ctBp)))
print(">>intra similarity scores for each community using Best Partition approach")
computingCosineSimilarity(ctBp, "ctBp")

print("\n>>inter similarity scores for each community using TF-IDF approach")
print("\t>>the average inter cosine similarity of TF-IDF is {}".format(intercosine(ctTf)))
print(">>intra similarity scores for each community using TF-IDF approach")
computingCosineSimilarity(ctTf, "ctTf")

print("\n>>inter similarity scores for each community using LDA approach")
print("\t>>the average inter cosine similarity of Lda is {}".format(intercosine(ctLda)))
print(">>intra similarity scores for each community using LDA approach")
computingCosineSimilarity(ctLda, "ctLda")

print("\n>>inter similarity scores for each community using Greedy approach")
print("\t>>the average inter cosine similarity of GA is {}".format(intercosine(ctGa)))
print(">>intra similarity scores for each community using Greedy approach")
computingCosineSimilarity(ctGa, "ctGa")

print()
print (len(simLis), len(interSumLis))
df1['IntraSimilarity'] = simLis 
df1['InterSimilarity'] = interSumLis #creating another coloumn in our results dataFrame similarity score of each community

Presentation.presenationOfResultDataframe(df1)

#trining to find what disimilar papers are talking about.
def disimilarPapers(ct):
    for com in ct:
        if len(ct[com]) < 2:
            print("hello")
            for paper in ct[com]:
                print(datasetdict[paper])

disimilarPapers(ctBp)

