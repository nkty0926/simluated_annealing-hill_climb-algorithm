'''
// Main File:        nqueens.py
// Semester:         CS 540 Fall 2020
// Authors:          Tae Yong Namkoong
// CS Login:         namkoong
// NetID:            kiatvithayak
// References:       TA's & Peer Mentor's Office Hours

'''
import random

# This function, when given a state of the board, return a list of lists, containing all valid successor states
# param: state : given state of board
# param: static_x : static x coord
# param: static_y : static y coord
def succ(state, static_x, static_y):
    succ_arr = [] # Generate list of lists
    if state[static_y] != static_x: # queen can't occupy same column
        return succ_arr
    for row in range(len(state)):  # iterate row
        for col in range(len(state)):  # iterate col
            copy_arr = state.copy() # copy array to compare for later
            if col == static_x:  # continue since can't move queen on static point
                continue
            if abs(copy_arr[col] - row) > 1:  # continue since we can only move one queen by one tile
                continue
            copy_arr[col] = row  # Xchange
            if copy_arr != state:  # Append if it is not same as state
                succ_arr.append(copy_arr)  # append successor state to returning list
    return sorted(succ_arr)

#This function, when given a state of the board, return an integer score such that the goal state scores 0
# param: state : given state of boards
def f(state):
    f_arr = [] # for storing f_scores
    for row in range(len(state)):
        for col in range(len(state)):
            if row != col:
                diagonal = row - col # get diagonal dist
                if state[col] == state[row]:  # check horizontal
                    if col not in f_arr: 
                        f_arr.append(col)
                elif state[col] == state[row] - diagonal or state[col] == state[row] + diagonal: # check diagonal
                    if col not in f_arr:  
                        f_arr.append(col)
    length = len(f_arr) # get length of arr to return f_score
    return length

#This function, when given the current state, use succ() to generate the successors and return the selected next state
# param: curr: current state of board
# param: static_x : static x coord
# param: static_y : static y coord
def choose_next(curr, static_x, static_y):
    next_arr = succ(curr, static_x, static_y) # get successor state from current state
    output = []
    if len(next_arr) == 0: # return none if state is invalid (no queen on static pt)
        return None
    next_arr.append(curr)
    minimum = f(next_arr[0]) # update minimum in for loop later
    for state in next_arr:
        temp = f(state)
        if temp == minimum: #if next state is the minimum
            output.append(state)
        elif temp < minimum: #if new minimum is found, then clear list and update min
            del output[:]
            output.append(state)
            minimum = temp
    output = sorted(output) # sort the list and return the first index
    return output[0]

#This function runs the hill-climbing algorithm from a given initial state, return the convergence state
# param: initial_state: given initial state of board
# param: static_x : static x coord
# param: static_y : static y coord
# param: print_path : flag to print or not print
def n_queens(initial_state, static_x, static_y, print_path = True):
    successor = initial_state # get initial state
    f_value = f(initial_state) # get f_value for initial state

    if print_path: #print only initial state
        print(initial_state, " - f=", f(initial_state), sep='')

    while f_value != 0: #while loop until f_value is not 0
        successor = choose_next(successor, static_x, static_y) #get next state
        successor_f = f(successor)  # get f value for next state
        if print_path:
            print(successor, " - f=", f(successor), sep='') # print next state
        if successor_f == f_value: # if duplicate f_value found break while loop
            break
        f_value = successor_f # get corresponding f_value
    return successor


#This function runs the hill-climbing algorithm on an n*n board with random restarts
# param: n: size of n x n board
# param: k: number of k restarts
# param: static_x : static x coord
# param: static_y : static y coord
def n_queens_restart(n, k, static_x, static_y):
    random.seed(1) #random seed
    count = 0
    output = []
    while count < k: # generate new random initial state and try again k times until f_value = 0 found
        current_state = []
        # generate state for random board of n x n size
        for i in range(n):
            if i == static_x:
                current_state.append(static_y)
            else:
                random_int = random.randint(0, n - 1)
                current_state.append(random_int)
        # get optimal state
        optimal = n_queens(current_state, static_x, static_y, print_path = False)
        f_value = f(optimal)
        output.append(optimal)

        # break if f_value of 0 is found
        if f_value == 0:
            print(optimal, " - f=", f(optimal), sep='')
            break

        count += 1 # increment count until count == k

    # sort and filter array for final output
    sorted_arr = sorted(output, key = lambda y: f(y))
    filtered_arr = filter(lambda x: f(x) == f(sorted_arr[0]), sorted_arr)
    final_arr = sorted(list(filtered_arr))

    for state in final_arr: # print the state and corresponding f scores
        print(state, " - f=", f(state), sep='')

