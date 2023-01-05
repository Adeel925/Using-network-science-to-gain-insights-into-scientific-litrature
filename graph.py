#for creating netowrks
import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms import community
from collections import Counter   
from collections import OrderedDict 
from numpy import array
import community
import matplotlib.pyplot as plt
from tqdm import tqdm

#create a bipartite graph
def createBgraph(nodePaper,nodewords,datasetdict,mode):
    #step 3 creating bipartite network
    B = nx.Graph()
    B.add_nodes_from(nodePaper, bipartite=0)
    B.add_nodes_from(nodewords, bipartite=1)
    #creating edges in the network
    for node in datasetdict:
        paperwords = datasetdict[node]
        #paperwords = list(dict.fromkeys(paperwords))
        for token in paperwords:
            if token in nodewords:
                B.add_edge(node, token)  
    
    #print(nx.is_connected(B))
    #making network of papers
    if(mode == True):
        G = bipartite.weighted_projected_graph(B,nodewords)
    else:
        G = bipartite.weighted_projected_graph(B,nodePaper)
    return G


# function to find the communites using Greedy algorithm 
def greedyApproch(G1,datasetdict):
    print('\n>> greedy algorithm partitioning process')
    ctd = list(nx.algorithms.community.greedy_modularity_communities(G1,weight='weight'))
    i =0
    ct ={}
    while i< len(ctd):
        if(i<20):
            #print("paperss in comunity = ",i," is = ", len(list(ctd[i])))
            ct[i]= list(ctd[i])
        i= i+1
    print("\t>>",'{0:<60}'.format("number of comunities using greedy algorithms"),'{0:<6}'.format(i))
    #topWordsCount(ct,datasetdict,True)
    return ct


def topWordsCount(ct,datasetdict, wordmap=False):
    comListcount = {}
    i = 0
    #counting words of number of top 10 communites 
    for pap in ct:
        lis = ct[pap]
        if(len(lis) < 2):
            continue
        comList = []
        for papa in lis:
            for w in datasetdict[papa]:
                comList.append(w)
        comListcount[i]=comList
        i= i+1
    if(wordmap == True):
        print("nil")
    else:
        return comListcount


def comparisonOfcommunites(comListcount):
    Lis = []
    for com in comListcount:
        dic = dict(Counter(comListcount[com]))
        dic_sorted_keys = sorted(dic, key=dic.get, reverse=True)
        dicComOthers = {}
        i = 0
        for word in dic_sorted_keys:
            comTopwords = []
            if i>5:
                break
            else:
                detail = (com, dic[word])
                comTopwords.append(dic[word])
                for comothers in comListcount:
                    if (comothers != com):
                        dicc = dict(Counter(comListcount[comothers]))
                        for wor  in dicc:
                            if (wor == word):
                                detail = (comothers, dicc[wor])
                                comTopwords.append(dicc[wor])
                                break
                            else:
                                continue
            i+=1
            dicComOthers[word] = comTopwords
        Lis.append(dicComOthers)
    return Lis
        

def comBest(G,datasetdict):
    print("\n>>Best parition partitioning process")
    partition=community.best_partition(G,resolution=0.97)
    ct = {}
    for paper in partition:
        if (not ct):
            ct[partition[paper]] = [paper]
        else:
            if(partition[paper] in ct.keys()):
                ct[partition[paper]].append(paper)
            else:
                ct[partition[paper]] = [paper]
                
    print("\t>>",'{0:<60}'.format("the total communites best partition has found are"),'{0:<6}'.format( len(ct)))
    mod = community.modularity(partition,G)
    print("\t>>",'{0:<60}'.format("Modularity: of best partition approach"),'{0:<6}'.format(mod))
    return ct


#function which is showing the basic network properties
def showBasicInfo(G):
    #displaying the basic properties of the network
    print(nx.info(G))
    print("Density : ",nx.density(G))


#saving the projections of single mode network as edge list and gexf format
def saveProjections(G):
    #papersNetwork creation 
    nx.write_weighted_edgelist(G,"test.weighted.edgelist", delimiter=',', encoding='utf-8')
    nx.write_gexf(G, "test.gexf")

#function for removing edges between paper having weight less then given one
def edgeRemovel(G,weight):
    edgeWeights = G.edges(data=True)
    remove = []
    for edge in edgeWeights:
        wi = (edge[2])
        #change this number to keep edges between the papers with higher value
        if(wi['weight']<weight):
            remove.append((edge[0], edge[1],edge[2]))
    #removing edges from the network to make it little sparser.
    for ed in remove:
        G.remove_edge(ed[0], ed[1])
    return G

#finding the patterns in network like basic properties and commnuity detctions 
def patterns(G,datasetdict):
    #Single Mode network graph information
    print("\n>> Before removel of edges from the network")
    showBasicInfo(G)
    
    weight = 6
    G = edgeRemovel(G,weight)
    
    print("\n>> After removel of edges from the network")
    showBasicInfo(G)
    #saveProjections(G)
    ct=comBest(G,datasetdict)
    return ct
        

        