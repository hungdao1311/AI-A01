from itertools import combinations
import random

def genRandomOp(n,k, all_matches):
    opponents = [[] for x in range(n)]
    random.shuffle(all_matches)
    for match in all_matches:
        if len(opponents[match[0]]) < k and len(opponents[match[1]]) < k:
            opponents[match[0]].append(match[1])
            opponents[match[1]].append(match[0])
    return opponents

def checkValidGen(opponents,k):
    for x in opponents:
        if len(x) != k:
            return False
    return True

def getMaxMinAvg(opponents,ranking, k,n):
    maxAvg = 0
    maxPlayer = 0
    minAvg = sum(list(map(lambda x: ranking[x],opponents[0])))/k
    minPlayer = 0
    for i in range(n):
        lst = list(map(lambda x: ranking[x],opponents[i]))
        avg = sum(lst)/k
        if avg > maxAvg:
            maxAvg = avg
            maxPlayer = i
        elif avg < minAvg:
            minAvg = avg
            minPlayer = i
    maxDiff = maxAvg - minAvg
    return [maxPlayer,minPlayer,maxDiff]


def swapOpponents(opponents,MaxMinPlayer,k):
    i = 0
    j = k-1
    while opponents[MaxMinPlayer[0]][j] == MaxMinPlayer[1] or opponents[MaxMinPlayer[0]][j] in opponents[MaxMinPlayer[1]]:
        j = j - 1
        if j < 0:
            return -1,-1
    while opponents[MaxMinPlayer[1]][i] == MaxMinPlayer[0] or opponents[MaxMinPlayer[1]][i] in opponents[MaxMinPlayer[0]]:
        i = i + 1
        if i > k-1:
            return -1,-1

    maxOp = opponents[MaxMinPlayer[0]].pop(j)
    minOp = opponents[MaxMinPlayer[1]].pop(0)

    opponents[MaxMinPlayer[0]].append(minOp)
    opponents[MaxMinPlayer[1]].append(maxOp)

    opponents[maxOp].remove(MaxMinPlayer[0])
    opponents[maxOp].append(MaxMinPlayer[1])

    opponents[minOp].remove(MaxMinPlayer[1])
    opponents[minOp].append(MaxMinPlayer[0])

    
    return maxOp,minOp

def main(file_input, file_output):
    #READ INPUT
    f_in = open(file_input)
    n,k = map(int,f_in.readline().split())
    ranking = list(map(int,f_in.read().split("\n")))
    f_in.close()
    all_matches = list(combinations(range(n),2))
    
    #GENERATE INITIAL DATA
    opponents = [[] for x in range(n)]
    while not checkValidGen(opponents, k):
        opponents = genRandomOp(n, k, all_matches)
    
    for x in opponents:
        x.sort(key=lambda x: ranking[x])
    # MaxMinPlayer = getMaxMinAvg(opponents,ranking,k,n)
    # maxDiff = MaxMinPlayer[2]
    # print(maxDiff)
    
    #RUN ALGORITHM
    while True:
        MaxMinPlayer = getMaxMinAvg(opponents,ranking,k,n)
        maxDiff = MaxMinPlayer[2]
        tmpOpponents = opponents[:]

        maxOp,minOp = swapOpponents(tmpOpponents, MaxMinPlayer,k)
        if(maxOp == -1):
            break
        for i in [maxOp,minOp, MaxMinPlayer[0],MaxMinPlayer[1]]:
            tmpOpponents[i].sort(key=lambda x: ranking[x])

        newMaxMin = getMaxMinAvg(tmpOpponents,ranking,k,n)
        newDiff = newMaxMin[2]
        
        if newDiff < maxDiff:
            opponents = tmpOpponents    
        else:
            break
    
    #WRITE OUPUT
    f_out = open("output.txt","w")
    for x in opponents:
        for y in x:
            f_out.write(str(y+1)+"\n")
    f_out.close()
    return
    

main('input.txt', 'output.txt')
