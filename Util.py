import copy
import random
import networkx as nx

def getK(G, t):

    dic = {}
    coreNums = nx.core_number(G)
    maxCoreNum = 1
    dictIndexMax = 0
    for key, values in coreNums.items():
        maxCoreNum = max(maxCoreNum, values)
        dictIndexMax = max(dictIndexMax, values)
        if  values in dic:
            dic[values] = dic[values]+1
        else:
            dic[values] = 1
    #cn - times

    i = maxCoreNum-1
    while i >= 0:
        if i not in dic:
            dic[i] = 0

        dic[i] = dic[i+1] + dic[i]
        i = i-1

    i = maxCoreNum
    while i >= 0:
        if dic[i] > t:
            break
        i = i-1
    return  i

def deleteALoop (graph, t, k):
    print("deleteA  start")
    if(len(graph.nodes) == t):
        return graph

    hasDel = True
    while hasDel:
        hasDel = False
        origin = list(graph.nodes)
        my_degrees = graph.degree()
        degree_dict = dict(my_degrees)
        for node in origin:
            if node not in list(graph.nodes):
                continue
            neighbors = graph.adj[node]

            flag_ThisNodeDegreeNotMeet = False
            for neighbor in neighbors:
                if degree_dict[str(neighbor)] <= k:
                    flag_ThisNodeDegreeNotMeet = True
                    break
            if (flag_ThisNodeDegreeNotMeet):
                continue

            g = copy.deepcopy(graph)
            for neighbor in neighbors:
                degree_dict[str(neighbor)] = degree_dict[str(neighbor)] - 1
            g.remove_node(node)

            flag = False

            CUR_NODES = []
            for cur_nodes in nx.connected_components(g):
                if len(cur_nodes) >= t:
                    flag = True
                    CUR_NODES = cur_nodes
                    break

            if (flag):
                graph.remove_node(node)
                hasDel = True
                if len(CUR_NODES) == 0:
                    continue
                graph = nx.Graph(graph.subgraph(CUR_NODES))
            else:
                for neighbor in neighbors:
                    degree_dict[str(neighbor)] = degree_dict[str(neighbor)] + 1

            if (len(graph.nodes) <= t):
                return graph

    return graph


def deleteOneInner(graph, t, k, total):
    nodelist = graph.nodes
    size = len(nodelist)
    if (size == t):
        return graph.nodes
    nodes = list(graph.nodes)

    for curNode in nodes:
        g = copy.deepcopy(graph)
        g.remove_node(curNode)
        coreGraphs = nx.k_core(g, k)
        afterDelHasK = False
        for cur in nx.connected_components(coreGraphs):
            if (len(cur) > t):
                afterDelHasK = True
                break
            elif (len(cur) == t):
                return cur
            else:
                continue
        if afterDelHasK:
            graph.remove_node(curNode)
    return None

def deleteB2(graph, t, k, total):
    # 获取图点的个数 如果正好等于t 直接返回
    nodelist = graph.nodes
    size = len(nodelist)
    if (size == t):
        return graph.nodes
    needDelete = size - t
    if(needDelete > size):
        return None

    g = graph.copy()
    deleteList = random.sample(nodelist, needDelete)
    g.remove_nodes_from(deleteList)
    coreGraphs = nx.k_core(g, k)

    for connectedPart in nx.connected_components(coreGraphs):
        if (len(connectedPart) == t):
            return list(connectedPart)

        g1 = graph.subgraph(connectedPart).copy()
        otherKNode = getAtLeastKNode(total, g1, k)

        # 往联通的部分加入点
        #终止条件 1、没有点可以加 2、长度恰好t
        while len(otherKNode) != 0 and len(g1.nodes) != t:
            #print("联通部分大小=%d, 固定大小t=%d, otherk = %d", len(list(g1.nodes)), t, len(otherKNode))
            minNode = min((t - len(list(g1.nodes))), len(otherKNode))
            print("本轮需要加入点", minNode)

            addNodes = random.sample(otherKNode, minNode)
            for i in range(0, minNode):
                addNodesToGraph(addNodes[i], g1, total)

            otherKNode = getAtLeastKNode(total, g1, k)
        #  当前联通部分如果ok 返回
        if len(g1.nodes) == t:
            return g1.nodes
    #end for，联通部分结束
    return None

def deleteB3(graph, t, k, total, outPath, hopeK):


    maxKCoreSize = getMaximalKCoreSize(total, k)
    g1 = graph
    otherKNode = getAtLeastKNode(total, g1, k)


    while len(otherKNode) != 0 :
        addNodes = otherKNode
        for i in range(0, len(otherKNode)):
            addNodesToGraph(addNodes[i], g1, total)
        otherKNode = getAtLeastKNode(total, g1, k)


    f = open(outPath, 'a')
    f.write("t= " + str(t) + "，find ans and k = "+str(hopeK) + ",act k= " + str(k) + "。continue add= " +str( len(g1.nodes)) +
            ", maximalKCoreSize = "+str(maxKCoreSize)+"\n")
    f.close()

    return None

def getMaximalKCoreSize(graph, k):
    #不断移除 度数<k的
    needDelete = 1
    nodelist = graph.nodes
    candidatelist = []

    while needDelete == 1:
        needDelete = 0
        for node in nodelist:
            if nx.degree(graph, node) >= k:
                candidatelist.append(node)
            else:
                needDelete = 1
        nodelist = candidatelist.copy()
        candidatelist = []
        graph = nx.subgraph(graph, nodelist)
    size = len(nodelist)
    return  size


def getAtLeastKNode(total, g, k):

    t1 = total.nodes
    t2 = g
    ans = []
    def isInG(n):
        return n not in t2

    t1 = filter(isInG, t1)

    for n in t1:

        if(total.degree(n) < k):
            continue
        count = 0

        for neigh in total.adj[n]:
            if neigh in g :
                count=count+1
        if(count >= k):
            ans.append(n)
    return  ans



def deleteNodesBiggerThanK(graph, k):
    NoBig = True
    while(True):
        for node in list(graph.nodes):
            if graph.degree(node) < k:
                NoBig = False
                graph.remove_node(node)
        if NoBig:

            break
        NoBig = True
    return graph


def addNodesToGraph(node, graph, total):
    neighbors = total.adj[node]
    nodes = list(graph.nodes)
    for neighbor in neighbors:
        if neighbor in nodes:
            graph.add_edge(neighbor, node)
