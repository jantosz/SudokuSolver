import logic


def run():
    choice = input()
    if choice.lower().strip() == 'preset':
        grid = _preset()
    else:
        grid = _take_initial_input()
    my_grid = logic.Grid(grid)
    _print_returned_grid(my_grid.solve())


def _preset():
    grid = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]]

    string_grid = []

    for row in grid:
        string_grid.append([])
        for col in row:
            if col == 0:
                string_grid[-1].append('0')
            else:
                string_grid[-1].append(str(col) + '*')

    return string_grid


def _take_initial_input():
    grid = []
    for i in range(9):
        row = []
        raw_string = input()
        for cell in raw_string:
            if cell == ' ':
                row.append('0')
            else:
                row.append(cell + '*')
        grid.append(row)
    return grid


def _print_returned_grid(grid):
    string = ''
    for row in grid:
        for cell in row:
            string += cell[0] + ' '
        string += '\n'
    print(string)


if __name__ == '__main__':
    run()
