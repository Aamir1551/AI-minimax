def printBoard(state):
    for i in range(3):
        print("|", end="")
        for j in range(3):
            if((i,j) in state[0]):
                print("x", end="|")
            elif((i,j) in state[1]):
                print("o", end="|")
            else: 
                print(" ", end="|")
        print("\n-------")


def isWin(state, playerID):
    winVertical = [True, True, True] 
    winHorizontal = [True, True, True] 
    winDiagonal = [True, True]

    for i in range(3):
        for j in range(len(winVertical)):
            winVertical[j] = winVertical[j] and ( (i,j) in state[playerID])
        for j in range(len(winHorizontal)):
            winHorizontal[j] = winHorizontal[j] and ( (j,i) in state[playerID]  )
        for j in range(len(winDiagonal)):
            winDiagonal[j] = winDiagonal[j] and ( (i, i if j==0 else (2-i)) in state[playerID])
    return any(winVertical) or any(winHorizontal) or any(winDiagonal)

def staticEvaluation(state):
    return (1 if isWin(state, 0) else (-1 if isWin(state, 1)  else 0)), state

def gameOver(state):
    return isWin(state, 0) or isWin(state, 1) or ( len(state[0]) + len(state[1]) == 9)

def getChildState(state, playerID):
    #playerID = 0 or 1, 0 is for x, 1 is for o
    [crosses, noughts] = state
    childStates =  []
    posTaken = set.union(crosses, noughts)
    for i in range(3):
        for j in range(3):
            if  not (i,j) in posTaken:
                if(playerID == 0):
                    childStates.append([set.union(crosses, {(i,j)}), noughts])
                if(playerID == 1):
                    childStates.append([crosses, set.union(noughts, {(i,j)})])
    return childStates


def minimax(state, depth, playerID):
    #player 0  tries to maximise value, while player 1 tries to minimise it
    if(depth == 0 or gameOver(state)):
        return staticEvaluation(state)
    
    stateChildren = getChildState(state, playerID)
    v, childChosen = 0, []
    
    
    if playerID == 0:
        v = float('-inf')
        for child in stateChildren:
            temp = minimax(child, depth -1, 1)            
            if(temp[0] > v):
                childChosen = child                
                v = temp[0]
        return v, childChosen
    
    if playerID == 1:
        v = float('inf')
        for child in stateChildren:
            temp = minimax(child, depth -1, 0)
            if(temp[0] < v):
                childChosen = child
                v = temp[0]
        
        return v, childChosen
    


print("Welcome to AI tic tac toe")
currentState = [set(), set()]  #initalState = [x coordinates, y coordinates]
printBoard(currentState)
while(not gameOver(currentState)):
    print("Enter Move (x,y): ")
    [x,y] = input().split(" ")

    while((int(x),int(y)) in set.union(currentState[0], currentState[1])):
        print("Sorry Location has already been taken")
        print("Enter Move: (x,y)")
        [x,y] = input().split(" ")
        
    currentState[0].add((int(x),int(y)))
    printBoard(currentState)
    print("AI's Turn")
    print("AI is thinking...")
    currentState = minimax(currentState, 9, 1)[1]
    printBoard(currentState)
if(isWin(currentState, 0)):
    print("Congratulations!, you win")
elif(isWin(currentState, 1)):
    print("AI wins, better luck next time")
else:
    print("Draw")



#exec(open('main.py').read())
