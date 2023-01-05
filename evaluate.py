import networkx as nx

# averegae degree weighted and simple
def averagedegree(subGraph):
    edgeNum = subGraph.edges()
    nodes =subGraph.nodes()
    avgDeg = 2*len(edgeNum)/ len(nodes)
    return avgDeg

def densityOfSub(subGraph):
    edgeNum = subGraph.edges()
    nodes =subGraph.nodes()
    density = len(edgeNum)/ (len(nodes)*(len(nodes) - 1 ) / 2)
    return density

#seprability simple and weihted
def sepratablity(subGraph, G):
    edgeNum = subGraph.edges()
    nodes =subGraph.nodes()
    totalEdges = G.edges(nodes)
    sepra = len(edgeNum)/(len(totalEdges)-len(edgeNum))
    return sepra


def clustering(subgraph):
    cc=nx.average_clustering(subgraph)
    return cc

def conductance(subGraph, G):
    edgeNum = subGraph.edges()
    nodes =subGraph.nodes()
    totalEdges = G.edges(nodes)
    conduct = (len(totalEdges)-len(edgeNum))/(2*len(edgeNum) + (len(totalEdges)-len(edgeNum)))
    return conduct


