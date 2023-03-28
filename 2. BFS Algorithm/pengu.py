'''
Logan Choi
Professor Morales
Intro to AI 
Puzzle #2
'''
from collections import deque
from pengu_func import *
        
'''
bfs() is searching for path using BFS
'''
def bfs(matrix,start):
    found = False
    frontier = [start]
    print("BFS STArt")
    #while frontier is not empty
    while len(frontier) != 0 and found == False:
        state = frontier.pop(0)
        if state.score >= 8:
            output(matrix,row,col,state)
            print("FOUND SOLUTION")
            found = True
            break

        #get list of valid moves
        valid_moves = get_valid_moves(matrix,state.pengu)
        
        #append the new set of states
        for m in valid_moves:
            newState = State()
            newState.deepcopy(state)
            make_move(m,matrix,newState)
            newState.moveStr += str(m)
            if not newState.dead:
                frontier.append(newState)
            elif newState.dead and newState.score >= 8:
                found = True
                print("Found Solution")
                output(matrix,row,col,newState)
                break


if __name__ == "__main__":
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
    bfs(matrix,start)