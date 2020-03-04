from __future__ import print_function
from os import system, name 
from sys import version_info, exit
if version_info[0] < 3:
    print("Must use python 3 to run program")
    exit(0)

#state = ({player1 pos}, {player 2 pos}, [m,n, heights], score)
#score represents who has won the game

def print_grid(state):
    (player1_pos, player2_pos, (m, n, heights), score) = state
    for i in range(m):
        print("     ", end="|")
        for j in range(n):
            if((i,j) in player1_pos):
                print("x", end="|")
            elif((i,j) in player2_pos):
                print("o", end="|")
            else:
                print("-", end="|")
        print()
    print("     |", end="")
    for i in range(n):
        print(str(i+1), end="|")
    print()

def calculate_score(state, playerID, new_piece):
    #update the game score, given person with playerID played last move
    (new_piece_i, new_piece_j) = new_piece
    (player1_pos, player2_pos, (m, n, heights), score) = state
    if(score != 0): return score

    horizotal_count = 0
    vertical_count = 0
    diagonal_count_l = 0
    diagonal_count_r = 0
    t = 0

    while( horizotal_count <4 and vertical_count <4 and diagonal_count_l <4 and diagonal_count_r < 4  and t <= 7):
        if((new_piece_i, new_piece_j - 3 + t ) in state[playerID]):
            horizotal_count +=1
        else:
            horizotal_count = 0
            
        if((t + new_piece_i -3, new_piece_j) in state[playerID]):
            vertical_count +=1
        else:
            vertical_count = 0

        if((new_piece_i - 3 + t, new_piece_j -3 + t) in state[playerID]):
            diagonal_count_l +=1
        else:
            diagonal_count_l = 0

        if((new_piece_i - 3 + t, new_piece_j + 3 -t) in state[playerID]):
            diagonal_count_r +=1
        else:
            diagonal_count_r = 0
        t+=1

    v  = any([horizotal_count == 4, vertical_count == 4, diagonal_count_l == 4, diagonal_count_r == 4])
    score = v if (playerID == 0) else -v
    return score


def static_evaluation(state):
    (player1_pos, player2_pos, (m, n, heights), score) = state
    return score

def game_over(state):
    (player1_pos, player2_pos, (m, n, heights), score) = state
    return score == 1 or score == -1 or (len(player1_pos) + len(player2_pos) == m*n)

def get_child_state(state, playerID):
    if(not playerID in {0,1}):
        print("Unexpected error")
        raise
    (player1_pos, player2_pos, (m, n, heights), score) = state
    child_states = []
    
    for j in range(n):
        new_location = get_input_location(j, heights)

        if(new_location[0] < 0):
            continue

        new_heights = []
        for h_i in range(len(heights)):
            new_heights.append(heights[h_i] if j != h_i else (heights[h_i] - 1))
        new_heights = tuple(new_heights)

        player_turn_positions = [player1_pos, player2_pos][playerID]
        player_turn_positions = frozenset.union(player_turn_positions, {new_location})

        new_player1_pos, new_player2_pos = player1_pos if playerID == 1 else player_turn_positions, player2_pos if playerID == 0 else player_turn_positions
        new_state = (new_player1_pos, new_player2_pos, (m, n, new_heights), score)

        new_score = calculate_score(new_state, playerID, new_location)
        new_state = (new_player1_pos, new_player2_pos, (m, n, new_heights), new_score)
        child_states.append(new_state)
    
    return child_states

def minimax(state, depth, playerID, states_visited):
    #player 0  tries to maximise value, while player 1 tries to minimise it
    #states visited is a hashmap from states to their minimax values
    if(state in states_visited):
        return states_visited[state]

    if(depth == 0 or game_over(state)):
        return static_evaluation(state), state
    
    state_children = get_child_state(state, playerID)
    v, child_chosen = 0, []
    
     
    if playerID == 0:
        v = float('-inf')
        for child in state_children:
            temp = minimax(child, depth -1, 1, states_visited)            
            if(temp[0] > v):
                child_chosen = child                
                v = temp[0]
    
    if playerID == 1:
        v = float('inf')
        for child in state_children:
            temp = minimax(child, depth -1, 0, states_visited)
            if(temp[0] < v):
                child_chosen = child
                v = temp[0]
    states_visited[state] = [v, child_chosen]
    return v, child_chosen
    

def get_input_location(col, heights):
    #heights describe how high each column is from the top of the grid
    return (heights[col], col)


def menu():
    print("Welcome to AI connect four!")
    print("If multiple inputs asked, enter them space seperated")
    print("Enter board size, m n (seperated by space): ", end="")

    [m, n] = input().split(" ")

    while(not m.isnumeric() or not n.isnumeric() or int(m)<4 or int(n)<4 or int(m)>10 or int(n)>10):
        print("Sorry, board sizes cannot be " + str(m) + "x" + str(n) + ".Sizes need to be between 5 and 10 inclusive")
        print("Enter board size, m n (seperated by space): ", end="")
        [m, n] = input().split(" ")
    [m, n] = [int(m), int(n)]

    clear()
    history = play_game(m, n)

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

def play_game(m, n):
    history = []
    states_visited = {}
    current_state = (frozenset(), frozenset(), (m, n, (m-1,) * n), 0)  #initial_state = [{player1 pos}, {player 2 pos}, [m,n], score]
    print()
    print_grid(current_state)
    print()
    print("Your Move first")
    print("To enter your move, type column number only")

    while(not game_over(current_state)):
        print()
        print("Enter Move: ", end="")
        col = input()
        (player1_pos, player2_pos, [m,n, current_heights], score) = current_state

        while(not col.isnumeric() or  int(col) >m or int(col) <1 or  get_input_location(int(col) -1, current_heights) in frozenset.union(player1_pos, player2_pos) or current_heights[int(col) -1] < 0):
            print("Sorry invalid input")
            print("Enter Move: ", end="")
            col = input()
            print("")

        col = int(col) - 1
        temp_heights = []
        for h_i in range(m):
            temp_heights.append(current_heights[h_i] - 1 if h_i == col else current_heights[h_i])

        location =  get_input_location(col, current_heights)
        current_state = (frozenset.union(player1_pos, frozenset({location})), player2_pos, (m,n,tuple(temp_heights)), score)
        score = calculate_score(current_state, 0, location)
        current_state = (frozenset.union(player1_pos, frozenset({location})), player2_pos, (m,n,tuple(temp_heights)), score)
        history.append(current_state)
    
        clear()
        print("AI's Turn")
        print("AI is thinking...")
        print()
        print_grid(current_state)
        solution = minimax(current_state, m*n, 1, states_visited)
        clear()

        current_state = solution[1]
        print("AI thinks he can win: " + str(solution[0] == 1))
        print()
        history.append(current_state)
        print_grid(current_state)



    print("Final grid")
    (player1_pos, player2_pos, (m,n, current_heights), score) = current_state
    print_grid(current_state)
    if(score == 1):
        print("Congratulations!, you win")
    elif(score == -1):
        print("AI wins, better luck next time")
    else:
        print("Draw")

menu()
#exec(open('main.py').read())
#try 6x7