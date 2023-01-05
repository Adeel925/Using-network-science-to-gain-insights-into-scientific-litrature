import graph
import networkx as nx
import community
import matplotlib.pyplot as plt
import NodeEmbeddings
from tqdm import tqdm

#computing first evaluation step
def computedegreecentrality(g,comNum):
    Deg = nx.degree_centrality(g)
    Deg_sorted_keys = sorted(Deg, key=Deg.get, reverse=True)
    pltdic = {}
    i = 0
    #sorting only keys of the dictionary words having degree centrality
    for deg in Deg_sorted_keys:
        if i < 10:
            pltdic[deg] = Deg[deg]
        i+=1
    #ploting of top 15 most central nodes
    plt.barh(range(len(pltdic)), pltdic.values(), align='center')
    plt.yticks(range(len(pltdic)), pltdic.keys())
    plt.xlabel('degree centrality', fontsize=12)
    plt.ylabel('keywords', fontsize=12)
    name = "/WnCm/degcen"+str(comNum)+".png"
    plt.savefig(name, format="PNG")
    plt.close()
    print(name, "top central nodes graph has been saved")
    return pltdic

def checkComQuality(comunities, datasetDict,start):
    i =0
    while i< len(comunities):
        
        if (len(comunities[i]) < 2):
            i+=1
            continue
        nodewords = []
        nodePapers = []
        for paper in list(comunities[i]):
            nodePapers.append(paper)
            for word in datasetDict[paper]:
                if word not in nodewords:
                    nodewords.append(word)
        G = graph.createBgraph(nodePapers,nodewords,datasetDict,True)
        weight = 2
        G = graph.edgeRemovel(G,weight) 
        computedegreecentrality(G,i)
        i+=1