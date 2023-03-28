'''
Logan Choi
Professor Morales
Intro to AI 
Puzzle #3
'''
import time
from pengu_func import *
        
'''
B_DFS() is actually using DFS with a depth limit
'''
def B_DFS(depth, matrix,row,col, start):
    frontier = [start]

    while len(frontier) != 0:
        #pop from most recently added
        state = frontier.pop()
        valid_moves = get_valid_moves(matrix,state.pengu)
        #if the length of the moveStr equals the depth, then 
        #check if you have obtained the score
        if len(state.moveStr) == depth:
            #if score obtained, output solution
            if state.score >= 16:
                print("FOUND SOLUTION")
                output(matrix,row,col,state)
                return True
        else:
            #for each valid_move in the current test state
            #append it
            for m in valid_moves:
                newState = State()
                newState.deepcopy(state)
                make_move(m,matrix,newState)
                newState.moveStr += str(m)
                #append if penguin is still alive
                if not newState.dead:
                    frontier.append(newState)
                #if penguin is dead but the score is 20, you found solution so output
                if newState.dead and newState.score >= 16:
                    print("Found Solution")
                    output(matrix,row,col,state)
                    return True
    #this means the solution has not been found and thus depth limit increments
    return False

'''
IDDFS() is searching for path using IDDFS
'''
def IDDFS(matrix,row,col,start):
    found = False
    depth = 0
    while True:
        print("ANOTHER ", depth)
        found = B_DFS(depth,matrix,row,col,start)
        if found == True:
            break
        depth = depth + 1
    return


if __name__ == "__main__":
    start_time = time.time()
    #Open input file
    fin = open(sys.argv[1],'r')

    #Get row and column
    row,col = fin.readline().split()
    row = int(row)
    col = int(col)

    #Get_board function will build the matrix and 
    #get penguin position
    matrix, pengu_pos, fishPos = get_board(row,col,fin)
    fin.close()

    start = State(pengu_pos, fishPos)
    #Play the game
    IDDFS(matrix,row,col,start)
    print("--- %s seconds ---" % (time.time() - start_time))

