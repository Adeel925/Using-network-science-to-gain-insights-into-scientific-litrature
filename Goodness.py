import evaluate
from beautifultable import BeautifulTable

def metrics(comunitydicc,G):  
    i= 0  
    table = BeautifulTable()
    table.column_headers = ["community number","total articles" ,"A-D", "Internal Dens" ,"Internal CC", "seprabiltiy", "conductance"]
    for c in comunitydicc:
        coms = comunitydicc[c]
        if len(coms) > 2:
            subGraph = G.subgraph(coms)
            avgDeg=evaluate.averagedegree(subGraph)
            density=evaluate.densityOfSub(subGraph) 
            cc = evaluate.clustering(subGraph)
            sepra=evaluate.sepratablity(subGraph, G)
            conductance = evaluate.conductance(subGraph,G)
            table.append_row([c,len(coms) ,avgDeg, density,cc, sepra ,conductance])
            i+=1
    print(table)
