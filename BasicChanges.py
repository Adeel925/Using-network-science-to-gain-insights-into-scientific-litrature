from collections import Counter
from collections import OrderedDict 

#the top most occured words in these papers.
def topwordsCount(datasetdict):
    allwords = []
    for wor in datasetdict:
        for wordd in datasetdict[wor]:
            allwords.append(wordd)
    dic = dict(Counter(allwords))
    sorted_dic = sorted(dic.items(), key=lambda kv: kv[1],reverse= True)
    i = 0
    worrd = []
    print("\n>>the top ten words from all papers are")
    for d in sorted_dic:
        if(i<10):
            print("\ttop ",i,"word = \t",d)
            worrd.append(d[0])
            i+=1
        else:
            break
    return worrd

#removing frequent words from the word list
def removewords(toptenwords,nodewords):
    #print ("length before  = ", len(nodewords))
    remaining = [x for x in nodewords if x not in toptenwords]
    #print ("length after removel  = ", len(remaining))      
    return remaining


#removing frequent words from the dataset dictionary
def removedatasetdict(toptenwords,datasetdict):
    for dat in datasetdict:
        #print ("length before  = ", len(datasetdict[dat]))
        remaining =[x for x in datasetdict[dat] if x not in toptenwords]
        datasetdict[dat] = remaining
        #print ("length after = ", len(datasetdict[dat]))
    return datasetdict

#basic information related to the dataset
def showingDataValues(data):
    print("\n")
    print(">> ",'{0:<60}'.format("the total length of dataset is"),'{0:<6}'.format(data.length))
    print(">> ",'{0:<60}'.format("length of nodes set of selected papers"),'{0:<6}'.format( len(data.nodePaper)))
    print(">> ",'{0:<60}'.format("length of nodes set of selected words:"), '{0:<6}'.format(len(data.nodewords)))
    print(">> ",'{0:<60}'.format("the null values in abstract are"),'{0:<6}'.format(data.getNullValuesInAbstract()))
    print(">> ",'{0:<60}'.format("Repeated abstract papers are") , '{0:<6}'.format(data.getRepeatedPapers()))
    