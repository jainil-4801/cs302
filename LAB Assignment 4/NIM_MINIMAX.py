from math  import inf
import sys
import copy
def get_array(): return list(map(int, sys.stdin.readline().strip().split()))
def get_ints(): return map(int, sys.stdin.readline().strip().split())
def input(): return sys.stdin.readline().strip()

sys.setrecursionlimit(10**6)
def nim_minimax(a,player):

    c=copy.deepcopy(a)
    c=list(c)
    c.sort()
    c=tuple(c)
    ##Check if the value of the state is already evaluated.
    if d[c,player]!=-2:
        return d[c,player]
    ##Base case
    if a[0]==0 and a[1]==0 and a[2]==0:

        if player%2==0:
            d[c,player]=-1
            return -1
        else:
            d[c,player]=1
            return 1
    if player%2==0:
        maxi=-1
    if player%2==1:
        mini=inf
    ##go through all the possible states.
    for i in range(len(a)):
        for j in range(1,a[i]+1):
            a[i]-=j
            if a[i]>=0:
                if player%2==0:
                    maxi=max(maxi,nim_minimax(a,(player+1)%2))
                if player%2==1:
                    mini=min(mini,nim_minimax(a,(player+1)%2))
            a[i]+=j
    if player%2==0:
        d[c,player]=maxi
        return maxi
    else:
        d[c,player]=mini
        return mini





d=dict()
print("Enter the number of objects in 3 piles ")

piles=get_array()


for i in range(piles[0]+1):
    for j in range(piles[1]+1):
        for k in range(piles[2]+1):
            state=[i,j,k]
            state.sort()
            state=tuple(state)
            #initially mark all the possible states as unvisited.
            d[state,0]=-2
            d[state,1]=-2




ans=(nim_minimax(piles,0))
if ans==1:
    print("Player 1 wins!")
else:
    print("Player 2 wins!")


###Input format:-
### x1 x2 x3