#!/usr/bin/env python3
# a0.py : Solve the N-Rooks, N-Queens & N-Knights problem! input nrook/nqueen/nknight
#importing the required libraries
import sys
import itertools

#from nrooks2 code
# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

#from nrooks2 code
# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

#from nrooks2 code
# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

#adapted from nrooks2 code
# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    if piece=='nrook':
        return "\n".join([ " ".join(["R" if col==1  else "X" if col==2 else "_" for col in row ]) for row in board])
    if piece=='nqueen':
        return "\n".join([ " ".join(["Q" if col==1  else "X" if col==2 else "_" for col in row ]) for row in board])
    if piece=='nknight':
        return "\n".join([ " ".join(["K" if col==1  else "X" if col==2 else "_" for col in row ]) for row in board])

#from nrooks2 code    
# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

#adapted from nrooks2 code
#get the diagnols attack squares of the queens on a board
def get_diagnols(board):
#getting the list of squares with queens    
  a=[[r,c] for r in range(0, N) for c in range(0,N) if board[r][c]==1]
#finding the diagnol squares for each queen and returning a list
  return [d for d in           
             [[d[0]-u,d[1]+u]  for u in range(1,N) for d in a] +
             [[d[0]+u,d[1]+u]  for u in range(1,N) for d in a] +        
             [[d[0]-u,d[1]-u]  for u in range(1,N) for d in a] +
             [[d[0]+u,d[1]-u]  for u in range(1,N) for d in a]              
          if 0 <= d[0] < N and 0 <= d[1] < N]

#get all knights attack squares on a board
#adapted the code to store cartesian product of lists from the link below  
#https://stackoverflow.com/questions/533905/get-the-cartesian-product-of-a-series-of-lists

def get_knightkills(board):
#getting the list of squares with knights    
  a=[[r,c] for r in range(0, N) for c in range(0,N) if board[r][c]==1]
#finding the attack squares for each knight and returning a list
  m = [i for i in itertools.product([-1,-2,1,2],[-1,-2,1,2]) if i[0]!=i[1] and abs(i[0])!=abs(i[1])]
  return [[d[0]+u[0],d[1]+u[1]] for u in m for d in a if 0 <= d[0]+u[0] < N and\
     0 <= d[1]+u[1] < N ]
#end point for the  above link
 
  
#getting the successor function
def successors_4(board):
        if piece=='nrook':
            return [add_piece(board, r, c)  for r in range(0, N) for c in range(0,N)\
                    if count_pieces(add_piece(board, r, c))<=N and\
                       board[r][c]!=1 and\
                       count_on_col(add_piece(board,r, c),c)<=1 and\
                       count_on_row(add_piece(board,r, c),r)<=1 and\
                       [r,c] not in un_sq_cds ]          
        elif piece=='nqueen': 
            return[add_piece(board, r, c)  for r in range(0, N) for c in range(0,N)\
                    if count_pieces(add_piece(board, r, c))<=N and\
                       board[r][c]!=1 and\
                       count_on_col(add_piece(board,r, c),c)<=1 and\
                       count_on_row(add_piece(board,r, c),r)<=1 and\
                       [r,c] not in un_sq_cds  and\
                       [r,c] not in get_diagnols(board) ] 
                          
        elif piece=='nknight':             
            return[add_piece(board, r, c)  for r in range(0, N) for c in range(0,N)\
                    if count_pieces(add_piece(board, r, c))<=N and\
                       board[r][c]!=1 and\
                       [r,c] not in un_sq_cds  and\
                       [r,c] not in get_knightkills(board) ]

# adapted from nrooks2 code
# check if board is a goal state
def is_goal(board):
    if piece == "nrook":      
        return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )
    
    if piece=="nqueen":        
        return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) and\
        all( [True for r in range(0, N) for c in range(0,N) if board[r][c]==1 and [r,c] not in get_diagnols(board) ])
        
    if piece=="nknight":        
        return count_pieces(board) == N and \
        all( [True for r in range(0, N) for c in range(0,N) if board[r][c]==1 and [r,c] not in get_knightkills(board) ])

#from nrooks2 code
# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors_4( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False


#picked up the conversion and storing multiple input in a list from the link below
#https://www.geeksforgeeks.org/input-multiple-values-user-one-line-python/ 
piece = sys.argv[1]
inputs = [int(x) for x in sys.argv[2:]]
N = inputs[0]
if len(inputs)>1:
    un_sq_cds = [inputs[i+2:i+4] for i in range(0,2*inputs[1],2)]
else:
    un_sq_cds = []

#end point for the code used in above link

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)
if len(un_sq_cds) > 0 and len(solution) > 0:
    for n in un_sq_cds:
      solution[n[0]][n[1]]=2 
print (printable_board(solution) if solution else "Sorry, no solution found. :(")


