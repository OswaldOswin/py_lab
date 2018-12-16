import random
n = 9

def group(values: list, n: int) -> list:
	a = []
	for i in range(0, len(values), n):
    	b = values[i:i+n]
    	a.append(b)
    return(a)



def read_sudoku(filename: str) -> list:
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid
  
print(read_sudoku(puzzle1.txt))