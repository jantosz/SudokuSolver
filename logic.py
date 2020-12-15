from copy import deepcopy


_DEBUG = False


class Grid:
    def __init__(self, grid: [[str]]):
        self._state = grid
        self._found = False
        if _DEBUG:
            self._counter = 0

    def solve(self) -> [[str]]:
        self._input_cell(0, 0)
        if not self._found:
            raise SolutionNotFoundError
        return deepcopy(self._state)

    def _input_cell(self, row, col):
        if _DEBUG:
            self._counter += 1
            print(f'RECURSIVE METHOD CALLED {self._counter} TIMES')

        while '*' in self._state[row][col]:
            #if _DEBUG:
            #    print('RUNNING PRESET NUMBERS LOOP')
            if row == 8 and col == 8:
                return
            if col == 8:
                row += 1
                col = 0
            else:
                col += 1

        if _DEBUG:
            print(f'ROW {row} COLUMN {col}')

        numbers_available = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        while not self._found:
            #if _DEBUG:
            #    print('RUNNING NOT FOUND LOOP')
            if len(numbers_available) == 0:
                self._state[row][col] = '0'
                return
            number = numbers_available[0]
            self._state[row][col] = str(number)
            if not self._erroneous():
                if self._is_full():
                    self._found = True
                    return
                else:
                    if col == 8:
                        new_row = row + 1
                        new_col = 0
                    else:
                        new_col = col + 1
                        new_row = row
                    self._input_cell(new_row, new_col)
            numbers_available.remove(number)

    def _is_full(self) -> bool:
        for row in range(9):
            for col in range(9):
                if self._state[row][col] == '0':
                    return False

        return True

    def _erroneous(self) -> bool:
        return self._check_row_errors() or self._check_col_errors() or self._check_group_errors()

    def _check_row_errors(self) -> bool:
        for row in range(9):
            cells_in_row = ''
            for col in range(9):
                if '*' in self._state[row][col]:
                    cells_in_row += self._state[row][col][0]

            if len(cells_in_row) != len(set(cells_in_row)):
                raise BadInputError('This puzzle is invalid.')

            for col in range(9):
                if '*' not in self._state[row][col] and self._state[row][col] != '0':
                    if self._state[row][col] in cells_in_row:
                        return True
                    else:
                        cells_in_row += self._state[row][col]

        return False

    def _check_col_errors(self) -> bool:
        for col in range(9):
            cells_in_col = ''
            for row in range(9):
                if '*' in self._state[row][col]:
                    cells_in_col += self._state[row][col][0]

            if len(cells_in_col) != len(set(cells_in_col)):
                raise BadInputError('This puzzle is invalid.')

            for row in range(9):
                if '*' not in self._state[row][col] and self._state[row][col] != '0':
                    if self._state[row][col] in cells_in_col:
                        return True
                    else:
                        cells_in_col += self._state[row][col]
            if _DEBUG:
                print(f'COL {col} CELLS IN COL: {cells_in_col}')

        return False

    def _check_group_errors(self) -> bool:
        error_1 = self._check_square_error(0, 3, 0, 3)
        error_2 = self._check_square_error(0, 3, 3, 6)
        error_3 = self._check_square_error(0, 3, 6, 9)
        error_4 = self._check_square_error(3, 6, 0, 3)
        error_5 = self._check_square_error(3, 6, 3, 6)
        error_6 = self._check_square_error(3, 6, 6, 9)
        error_7 = self._check_square_error(6, 9, 0, 3)
        error_8 = self._check_square_error(6, 9, 3, 6)
        error_9 = self._check_square_error(6, 9, 6, 9)

        return error_1 or error_2 or error_3 or error_4 or error_5 or error_6 or error_7 or error_8 or error_9

    def _check_square_error(self, row_start, row_stop, col_start, col_stop) -> bool:
        cells_in_group = []
        for row in range(row_start, row_stop):
            for col in range(col_start, col_stop):
                if '*' in self._state[row][col]:
                    cells_in_group.append(self._state[row][col][0])

        if len(cells_in_group) != len(set(cells_in_group)):
            raise BadInputError('This puzzle is invalid.')

        for row in range(row_start, row_stop):
            for col in range(col_start, col_stop):
                if '*' not in self._state[row][col] and self._state[row][col] != '0':
                    if self._state[row][col] in cells_in_group:
                        return True
                    else:
                        cells_in_group.append(self._state[row][col])

        return False


class BadInputError(Exception):
    pass


class SolutionNotFoundError(Exception):
    pass
