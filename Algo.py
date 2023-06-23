import time
import networkx as nx
from Util import *
from SGreedy import *
# data correspond to which?
def getDataPathAndAlgoChoose(dataDict, algoDict, dataChoice, algoChoice):
    pathWin = r""
    outWin = r""
    if dataChoice == 1:
        pathWin = r"data/email-Enron_36692/Email-Enron.txt"
        outWin = r"data/email-Enron_36692/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 2:
        pathWin = r"data/lastfm_asia/lastfm_asia_edgesTrans.txt"
        outWin = r"data/lastfm_asia/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 3:
        pathWin = r"data/p2p8/p2p-Gnutella08.txt"
        outWin = r"data/p2p8/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 4:
        pathWin = r"data/DBLP_317080/com-dblp.ungraph.txt"
        outWin = r"data/DBLP_317080/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 5:
        pathWin = r"data/HepPh_34546/Cit-HepPh.txt"
        outWin = r"data/HepPh_34546/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 6:
        pathWin = r"data/gplus_107614/gplus_combined.txt"
        outWin = r"data/gplus_107614/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 7:
        pathWin = r"data/smallGraph/arenas-email_5451/arenas-email.txt"
        outWin = r"data/smallGraph/arenas-email_5451/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 8:
        pathWin = r"data/smallGraph/friend_12534/friend.txt"
        outWin = r"data/smallGraph/friend_12534/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 9:
        pathWin = r"data/smallGraph/moreno_innovation_1000/moreno.txt"
        outWin = r"data/smallGraph/moreno_innovation_1000/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 10:
        pathWin = r"data/smallGraph/yeast_2277/yeast.txt"
        outWin = r"data/smallGraph/yeast_2277/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 11:
        pathWin = r"data/youtube_1134890/com-youtube.ungraph.txt"
        outWin = r"data/youtube_1134890/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 12:
        pathWin = r"data/application/humanProtein/maayan-Stelzl/protein.txt"
        outWin = r"data/application/humanProtein/maayan-Stelzl/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 13:
        pathWin = r"data/application/protein2_maayan/maayan-pdzbase.txt"
        outWin = r"data/application/protein2_maayan/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]
    elif dataChoice == 14:
        pathWin = r"data/smallGraph/subgraph/subgraph_10Core.txt"
        outWin = r"data/smallGraph/subgraph/" + algoDict[algoChoice] + "_" + dataDict[dataChoice]

    return pathWin, outWin

def processTopDown(G, savePath, t):

    k = getK(G, t)
    k1 = k
    k = min(t - 1, k);
    T1 = time.time()
    ans, delStatus, k = criticalKcoreDelOne(k, G, t)
    if ans == None:
        k = 0
    T2 = time.time()
    print('cost:%s s' % ((T2 - T1)))

    f = open(savePath, 'a')
    strings = str(T2 - T1)
    f.write("size= " + str(t) + ",origink= " + str(k1) + ",k= " + str(k) + ",at "+delStatus +" end， time= " + strings + "s\n");
    f.close()

def criticalKcoreDelOne(k, G, t):

    while k >= 1:
        G1 = copy.deepcopy(G);
        G1 = deleteNodesBiggerThanK(G1, k);

        coreGraphs = nx.k_core(G1, k);
        for cur in nx.connected_components(coreGraphs):
            if len(cur) == t:
                return cur, "find k core", k;
            elif len(cur) < t:
                continue;
            else:
                gcur = nx.Graph(nx.subgraph(G1, cur))
                p1 = deleteALoop(gcur, t, k);
                if (len(p1.nodes) == t):
                    return p1.nodes, "critical", k;

                p2 = deleteOneInner(p1, t, k, G);
                if p2 == None:
                    continue;
                if (len(p2) == t):
                    return p2, "algo2", k;
        k = k - 1;
    return None, "not find", k

def processBottomUp(G, savePath, t):
    k = getK(G, t)
    k1 = k
    k = min(t - 1, k);
    T1 = time.time()

    ans, originK, k = OnlykCoreRandomKcore(k, G, t)
    if ans == None:
        k = 0
    maxk = k
    # try more times
    if k1 != k:
        for i in range(0, 4):
            ans, originK, k = OnlykCoreRandomKcore(k, G, t)
            if ans == None:
                k = 0
            maxk = max(maxk, k)
            if k1 == k:
                break
    k = maxk
    T2 = time.time()
    print('time:%s s' % ((T2 - T1)))

    f = open(savePath, 'a')
    strings = str(T2 - T1)
    f.write("size= " + str(t) + ",origink= " + str(k1) + ",k= " + str(k) + ",time= " + strings + "s\n");
    f.close()

def OnlykCoreRandomKcore(k, G, t):
    originK = k
    graphs = []
    while k >= 1:
        coreGraphs = nx.k_core(G, k);
        for cur in nx.connected_components(coreGraphs):
            if len(cur) < t:
                continue
            elif len(cur) == t:
                return cur, originK, k

            gcur = nx.Graph(nx.subgraph(G, cur))
            deleteList = random.sample(list(cur), len(cur) - t)
            gcur.remove_nodes_from(deleteList)

            coreGraphs = nx.k_core(gcur, k);
            for connectedPart in nx.connected_components(coreGraphs):
                if (len(connectedPart) == t):
                    return cur, originK, k
                else:
                    graphs.append(nx.subgraph(gcur, connectedPart))


            curGraphList = graphs.copy()
            for graph in curGraphList:
                g1 = graph.copy()
                otherKNode = getAtLeastKNode(G, g1, k);

                while len(otherKNode) != 0 and len(g1.nodes) != t:
                    minNode = min((t - len(list(g1.nodes))), len(otherKNode))
                    addNodes = random.sample(otherKNode, minNode)
                    for i in range(0, minNode):
                        addNodesToGraph(addNodes[i], g1, G)
                    otherKNode = getAtLeastKNode(G, g1, k);

                if len(g1.nodes) == t:
                    return cur, originK, k
                else:
                    graphs.append(g1)
        k = k - 1
    return None, originK, 0

def processCritical(G, savePath, t):

    k = getK(G, t)

    k = min(t - 1, k);
    T1 = time.time()
    ans, originK, k = criticalKcore(k, G, t)

    if ans == None:
        k = 0
    T2 = time.time()
    print('time:%s s' % ((T2 - T1)))

    f = open(savePath, 'a')
    strings = str(T2 - T1)
    f.write("size= " + str(t) + ",origink= " + str(originK) + ",k= " + str(k) + ",time= " + strings + "s\n");
    f.close()
def criticalKcore(k, G, t):

    originK = k
    while k >= 1:
        G1 = copy.deepcopy(G)
        G1 = deleteNodesBiggerThanK(G1, k)

        coreGraphs = nx.k_core(G1, k)
        for cur in nx.connected_components(coreGraphs):
            if len(cur) == t:
                return cur, originK, k
            elif len(cur) < t:
                continue
            else:
                gcur = nx.Graph(nx.subgraph(G1, cur))
                p1 = deleteALoop(gcur, t, k)
                if (len(p1.nodes) == t):
                    return p1.nodes, originK, k

                p2 = deleteB2(p1, t, k, G)

                if p2 == None:
                    continue
                if (len(p2) == t):
                    return p2, originK, k
        k = k - 1
    return None, originK, k

def processSgreedy(G, runPath, savePath, t):

    T1 = time.time()
    originK, ans = RunSGreedy(G, runPath, t)
    T2 = time.time()

    if ans == None:
        ansK = 1
    else:
        subG = nx.subgraph(G, ans)
        ansK = t
        for node in subG.nodes:
            tmp = nx.degree(subG, node)
            if tmp < ansK:
                ansK = tmp

    f = open(savePath, 'a')
    strings = str(T2 - T1)
    f.write("size= " + str(t) + ",origink= " + str(originK) + ",k= " + str(ansK) + ",time= " + strings + "s\n");
    f.close()
def processContinueAdd(G, savePath, t):
    k = getK(G, t)
    k = min(t - 1, k);
    ans, originK, k = OnlykCoreRandomKcore(k, G, t)
    if ans == None:
        k = 0
    f = open(savePath, 'a')
    partialSolution = nx.subgraph(G, ans).copy()
    deleteB3(partialSolution, t, k, G, savePath, originK)
    # f.write("size= " + str(t) + ",origink= " + str(originK) + ",k= " + str(k) + "s\n");
    f.close()
