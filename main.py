# coding=utf-8
from Algo import *

dataDict = {1: "email.txt", 2: "lastfm.txt", 3: "p2p8.txt", 4: "dblp.txt", 5: "hepph.txt", 6: "gplus.txt",
            7: "arenas-email.txt", 8: "friend.txt", 9: "moreno.txt", 10: "yeast.txt",
            11: "youtube.txt", 12: "protein.txt", 13: "protein2_maayan", 14: "subg-10Core"}
algoDict = {1: "top down", 2: "bottom up", 3: "critical", 4: "s greedy", 5: "case study:continue"}
# choose which algo and data to run?
dataChoice = 8
algoChoice = 2

pathWin, outWin = getDataPathAndAlgoChoose(dataDict, algoDict, dataChoice, algoChoice)

# read graph
G = nx.read_edgelist(pathWin)
G.remove_edges_from(nx.selfloop_edges(G))

size = int(len(G) * 0.9)
start = int(size * 0.1)
dis = int((size - start) / 50)
if dis == 0:
    dis = 1

if algoChoice == 1:
    for t in range(start, size, dis):
        G1 = copy.deepcopy(G)
        processTopDown(G1, outWin, t)
elif algoChoice == 2:
    for t in range(start, size, dis):
        G1 = copy.deepcopy(G)
        processBottomUp(G, outWin, t)
elif algoChoice == 3:
    for t in range(start, size, dis):
        G1 = copy.deepcopy(G)
        processCritical(G1, outWin, t)
elif algoChoice == 4:
    for t in range(start, size, dis):
        G1 = copy.deepcopy(G)
        processSgreedy(G, pathWin, outWin, t)
elif algoChoice == 5:
    for t in range(start, size, dis):
        G1 = copy.deepcopy(G)
        processContinueAdd(G1, outWin, t)
