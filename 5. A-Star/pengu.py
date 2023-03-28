'''
Logan Choi
Professor Morales
Intro to AI 
Puzzle #2
'''
import heapq as hq
import time
from pengu_func import *
        
'''
ASTAR() is searching for path using ASTAR
'''
def ASTAR(matrix,start,totalFish):
    found = False
    frontier = [start]
    hq.heapify(frontier)
    print("ASTAR")
    #while frontier is not empty
    while len(frontier) != 0 and found == False:
        state = hq.heappop(frontier)
        if state.score == totalFish:
            output(matrix,row,col,state)
            print("FOUND SOLUTION")
            found = True
            break

        #get list of valid moves
        valid_moves = get_valid_moves(matrix,state.pengu)
        
        #append the new set of states if not dead
        for m in valid_moves:
            newState = State()
            newState.deepcopy(state)
            make_move(m,matrix,newState)
            newState.moveStr += str(m)
            if not newState.dead:
                hq.heappush(frontier,newState)


if __name__ == "__main__":
    #Open input file
    startTime = time.time()
    fin = open(sys.argv[1],'r')

    #Get row and column
    row,col = fin.readline().split()
    row = int(row)
    col = int(col)

    #Get_board function will build the matrix and 
    #get penguin position
    matrix, pengu_pos,fish = get_board(row,col,fin)
    fin.close()

    start = State(pengu_pos,fish)
    print(fish)
    #Play the game
    ASTAR(matrix,start,fish)
    print("--- %s seconds ---" % (time.time() - startTime))