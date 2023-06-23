import heapq

from Util import *
import copy
import time

import networkx as nx
#  s greedy
def RunSGreedy(G, path, t):

    # step 2-3
    k = getK(G, t)
    originK = k

    ans = tryAdd(G, k, t)
    return originK, ans

def getOtherNodesNotInGraph(total, graph, k):
    neighborSet = set()
    for node in graph:
        neighborSet = neighborSet.union(set(total.adj[node]))
    ansSet = neighborSet - set(graph)
    ans = set()
    for n1 in ansSet:
        if total.degree(n1) < k:
            continue
        ans.add(n1)
    return ans


#  core implement of sgreedy
def tryAdd(total, k, t):
    length = len(total.nodes)
    randomStart = random.randint(0, length - 1)
    # partialSolution
    partialSolution = set()
    partialSolution.add(list(total.nodes)[randomStart])

    partialDegreeDic = {}
    partialDegreeDic[list(total.nodes)[randomStart]] = 0

    if len(partialSolution) ==  t:
        return partialSolution

    while len(partialSolution) != t:

        candidateNode = getOtherNodesNotInGraph(total, partialSolution, k)

        if len(candidateNode) == 0:
            if (len(partialSolution)) == t:
                return partialSolution
            else:
                return None
        highNode = getHighScoreNode(candidateNode, partialSolution, total, k, partialDegreeDic)
        partialSolution.add(highNode)
        neighbors = nx.neighbors(total, highNode)
        highNodeDegree = 0
        for neighbor in neighbors:
            if neighbor in partialSolution:
                partialDegreeDic[neighbor] = partialDegreeDic[neighbor]+1
                highNodeDegree = highNodeDegree + 1
        partialDegreeDic[highNode] = highNodeDegree
    if len(partialSolution) == t:
        return partialSolution
    return None


def getHighScoreNode(candidateNode, partialSolution, total, k, partialDegreeDic):

    ansNode = None
    ansScore = 0
    for ps in candidateNode:
        p1_score = p1(partialSolution, total, k, ps, partialDegreeDic)
        p2_score = p2(partialSolution, total, k, ps)
        if (ansNode == None) or (p1_score - p2_score > ansScore):
            ansNode = ps
            ansScore = p1_score - p2_score

    return ansNode

# represent p+
def p1(graph, total, k, u, partialDegreeDic):

    ans = 0

    setGraph = set(graph)
    nodeList = set(list(total.adj[u]))
    for node in nodeList:

        if node in setGraph and partialDegreeDic[node] < k:
            ans = ans + 1
    return ans

# represent P-
def p2(graph, total, k, u):
    listTotal = list(total.adj[u])
    count = 0
    setGraph = set(graph)
    for listNum in listTotal:
        if listNum in setGraph:
            count = count + 1
    return max(k - count, 0)
