import random
import time
import sys
import statistics

# used to print the board
def print_board(arr):
	for i in range(9):
		for j in range(9):
			print(arr[i][j], end = " ")
		print()

# Checks value against constraints
def valid(board, row, col, value):

	# Checking row constraint
	for x in range(9):
		if board[row][x] == value:
			return False

	# Checking column constraint
	for x in range(9):
		if board[x][col] == value:
			return False

	# Check box constraint
	startRow = row - row % 3
	startCol = col - col % 3
	for i in range(3):
		for j in range(3):
			if board[i + startRow][j + startCol] == value:
				return False
	return True

# Solves the sudoku using backtracking
def solve_backtracking(board, empty_blocks, position):
	#checking if puzzle solved
	if len(empty_blocks) == position:
		return True
	
	global counter
    #counter counts the number of times the function was called, counting the moves it makes 
	counter += 1
	
	value_list = [1,2,3,4,5,6,7,8,9]
	random.shuffle(value_list)
	temp = empty_blocks[position]
	for num in value_list:
		if valid(board, temp[0], temp[1], num):
			board[temp[0]][temp[1]] = num
			if solve_backtracking(board, empty_blocks, position + 1):
				return True

		board[temp[0]][temp[1]] = 0
	return False

# forward checks the remaining empty blocks, returns false if no value left for any cell
def forward_check(board, empty_blocks, position):
    for i in range(position + 1, len(empty_blocks)):
        remaining_values = []
        for value in range(1,10):
            temp = empty_blocks[i]
            if valid(board, temp[0], temp[1], value):
                remaining_values.append(value)
                break
        if len(remaining_values) == 0:
            return False
    return True

# solves the sudoku using forward checking and backtracking
def solve_forwardchecking(board, empty_blocks, position):
    #checking if puzzle solved
	if len(empty_blocks) == position:
		return True
	
	global counter
    #counter counts the number of times the function was called, counting the moves it makes 
	counter += 1
	temp = empty_blocks[position]
	value_list = [1,2,3,4,5,6,7,8,9]
	random.shuffle(value_list)
	for num in value_list:
		if valid(board, temp[0], temp[1], num):
			board[temp[0]][temp[1]] = num
			if forward_check(board, empty_blocks, position):
				if solve_forwardchecking(board, empty_blocks, position + 1):
					return True
			board[temp[0]][temp[1]] = 0
	return False           

# returns a list of empty blocks along with their possible values. Checks for Most constraining variable and Most constrained variable
def find_remaining_list(board):
    remaining_values = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                temp = 0
                for k in range(1,10):
                    if valid(board, i, j, k):
                        temp += 1
                remaining_values.append([i, j, temp])
    return remaining_values
    
# returns a list of values for a block along with the number of constraints on each. Checks for Least Constraining Value
def find_lcv(board, mcv_list, mcv_block):
    lcv_list = []
    for k in range(1, 10):
        if valid(board, mcv_block[0], mcv_block[1], k):
            board[mcv_block[0]][mcv_block[1]] = k
            temp = 0
            for i in mcv_list:
                if not valid(board, i[0], i[1], k):
                    temp += 1
            lcv_list.append([k, temp])
            board[mcv_block[0]][mcv_block[1]] = 0
    return lcv_list

# Solves the sudoku using 3 Heuristics, Forward checking and back tracking
def solve_heuristic(board):
    mcv_list = find_remaining_list(board)
    #checking if puzzle is solved
    if len(mcv_list) == 0:
        return True

    mcv_block = min(mcv_list, key = lambda x : x[2])
    global counter 
    counter += 1
    value_list = find_lcv(board, mcv_list, mcv_block)
    value_list.sort(key = lambda x : x[1])
    for num in value_list:
        board[mcv_block[0]][mcv_block[1]] = num[0]
        if solve_heuristic(board):
            return True
        board[mcv_block[0]][mcv_block[1]] = 0
    return False

# returns the list of empty blocks on the board
def find_empty_blocks(board):
    empty_blocks = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_blocks.append( [i,j] )
    random.shuffle(empty_blocks)

    return empty_blocks

# main
if len( sys.argv ) < 4:
    print("Implement using: python sudoku.py <level = 1,2,3,4> <method = 1,2,3> <number of trials") 
else:
    trails = int(sys.argv[3])
    meathod = int(sys.argv[2])
    counts = []
    times = []
    for i in range(trails):
        board_easy = [[0,5,8,0,6,2,1,0,0],[0,0,2,7,0,0,4,0,0],[0,6,7,9,0,1,2,5,0],[0,8,6,3,4,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,7,6,8,9,0],[0,2,9,6,0,8,7,4,0],[0,0,3,0,0,4,9,0,0],[0,0,5,2,9,0,3,8,0]]
        board_medium = [[8,3,0,6,0,0,0,0,7],[0,0,7,0,2,0,0,5,0],[0,2,1,0,0,9,0,8,0],[6,0,0,0,8,0,0,0,9],[0,0,0,4,6,5,0,0,0],[3,0,0,0,9,0,0,0,2],[0,8,0,2,0,0,3,9,0],[0,5,0,0,4,0,2,0,0],[2,0,0,0,0,8,0,1,6]]
        board_hard = [[1,0,0,0,3,0,0,0,0],[0,6,2,0,0,0,0,0,0],[0,0,0,7,0,2,8,0,4],[0,7,0,1,4,0,0,0,2],[0,4,0,0,0,0,0,9,0],[8,0,0,0,5,6,0,7,0],[6,0,9,8,0,7,0,0,0],[0,0,0,0,0,0,2,1,0],[0,0,0,0,6,0,0,0,9]]
        board_evil = [[0,1,0,0,0,0,0,0,6],[9,0,0,2,0,0,0,0,0],[7,3,2,0,4,0,0,1,0],[0,4,8,3,0,0,0,0,2],[0,0,0,0,0,0,0,0,0],[3,0,0,0,0,4,6,7,0],[0,9,0,0,3,0,5,6,8],[0,0,0,0,0,2,0,0,1],[6,0,0,0,0,0,0,3,0]]
        boards = [board_easy, board_medium, board_hard, board_evil]
        board = boards[int(sys.argv[1]) - 1]

        counter = 0
        start = time.time()
        empty_blocks = find_empty_blocks(board)
        if meathod == 1:
            solve_backtracking(board, empty_blocks, 0)
        elif meathod == 2:
            solve_forwardchecking(board, empty_blocks, 0)
        else:
            solve_heuristic(board)
        end = time.time()
        times.append((end - start)*1000)
        counts.append(counter)

    print("Sudoku was solved, results:")
    print(boards[int(sys.argv[1]) - 1])

    nodes_avg = sum(counts)/trails
    time_avg = sum(times)/trails
    nodes_std = statistics.stdev(counts)
    time_std = statistics.stdev(times)
    print(f"completed in moves: {nodes_avg} + {nodes_std}")
    print(f"completed in time(milliseconds): {time_avg} + {time_std}")



