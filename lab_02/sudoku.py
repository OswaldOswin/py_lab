import random


def group(values: list, n: int) -> list:
    return [values[i:i + n] for i in range(0, len(values), n)]


def read_sudoku(filename: str) -> list:
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values: list):
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def get_row(values: list, pos: tuple) -> list:
    return values[pos[0]]


def get_col(values: list, pos: tuple) -> list:
    return [values[row][pos[1]] for row in range(len(values))]


def get_block(values: list, pos: tuple) -> list:
    block = []
    r = 3 * (pos[0] // 3)
    c = 3 * (pos[1] // 3)
    for i in range(3):
        for j in range(3):
            block.append(values[r+i][c+j])
    return block


def find_empty_positions(grid: list) -> tuple:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '.':
                return (row, col)

    return (-1, -1)


def find_possible_values(grid: list, pos: tuple) -> set:
    a = set('123456789')
    b = set(get_block(grid, pos))
    c = set(get_col(grid, pos))
    d = set(get_row(grid, pos))
    e = a - b - c - d
    return e


def solve(grid: list) -> list:
    pos = find_empty_positions(grid)
    if pos == (-1, -1):
        return grid
    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[row][col] = '.'
    return []


def check_solution(solution: list) -> bool:
    for row in range(len(solution)):
        values = set(get_row(solution, (row, 0)))
        if values != set('123456789'):
            return False

    for col in range (len(solution)):
        values = set(get_col(solution, (0, col)))
        if values != set('123456789'):
            return False

    for row in (0, 3, 6):
        for col in (0, 3, 6):
            values = set(get_block(solution, (row, col)))
            if values != set('123456789'):
                return False
    return True


def generate_sudoku(N: int) -> list:
    grid = solve([['.'] * 9 for _ in range(9)])
    N = 81 - min(81, N)
    while N > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            N -= 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
