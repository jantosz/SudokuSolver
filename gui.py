import tkinter
import logic


_DEFAULT_FONT = ('Helvetica', 50)


class SudokuResult:
    def __init__(self, result):
        self._window = tkinter.Tk()
        self._window.configure(bg='black')
        self._window.wm_title('Solution')
        try:
            self._window.iconbitmap('icon.ico')
        except:
            pass
        self._board = result

    def display(self):
        self._create_display()
        self._window.mainloop()

    def _create_display(self):
        for row in range(9):
            self._window.rowconfigure(row, weight=1)
            for col in range(9):
                padx1 = 0
                pady1 = 0
                padx2 = 0
                pady2 = 0
                if row == 2 or row == 5:
                    pady2 = 2
                if row == 3 or row == 6:
                    pady1 = 2
                if col == 2 or col == 5:
                    padx2 = 2
                if col == 3 or col == 6:
                    padx1 = 2

                if '*' in self._board[row][col]:
                    text_color = 'black'
                else:
                    text_color = 'blue'

                self._window.columnconfigure(col, weight=1)
                label = tkinter.Label(master=self._window, text=self._board[row][col][0],
                                      font=_DEFAULT_FONT, bg='white', width=2, borderwidth=1, relief='solid',
                                      fg=text_color)
                label.grid(row=row, column=col, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S,
                           padx=(padx1, padx2), pady=(pady1, pady2))


class SudokuInput:
    def __init__(self):
        self._grid = None
        self._window = tkinter.Tk()
        self._window.wm_title('Sudoku Solver')
        try:
            self._window.iconbitmap('icon.ico')
        except:
            pass
        self._entries = []
        self._add_all_entries()

        self._labeltext = tkinter.StringVar()
        self._labeltext.set('Awaiting input...')

        self._status_label = tkinter.Label(master=self._window, font=('Helvetica', 10), textvariable=self._labeltext)
        self._solve_button = tkinter.Button(master=self._window, font=('Helvetica', 20), text='SOLVE',
                                            command=self._solve)

        self._status_label.grid(row = 9, column=0, columnspan=3, sticky=tkinter.W + tkinter.S, padx=5, pady=5)
        self._solve_button.grid(row=9, column=3, columnspan=3, padx=10, pady=10,
                                sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)

    def run(self):
        self._window.mainloop()

    def _solve(self):
        self._update_text_to_solve()
        self._solve_puzzle()

    def _update_text_to_solve(self):
        self._labeltext.set('Solving...')

    def _solve_puzzle(self):
        for row in self._entries:
            for cell in row:
                if cell.get() != '':
                    try:
                        int(cell.get())
                    except ValueError:
                        self._labeltext.set('Invalid input!')
                        return
                    if int(cell.get()) < 1 or int(cell.get()) > 9:
                        self._labeltext.set('Invalid input!')
                        return

        self._create_grid()

        try:
            solution = self._grid.solve()
        except logic.BadInputError:
            self._labeltext.set('This is not a valid Sudoku.')
            return
        except logic.SolutionNotFoundError:
            self._labeltext.set('ERROR: Could not solve.')
            return

        self._labeltext.set('Solved.')
        SudokuResult(solution).display()


    def _create_grid(self):
        board = []
        for row in self._entries:
            board.append([])
            for cell in row:
                cell_input = cell.get()
                if cell_input == '':
                    board[-1].append('0')
                else:
                    board[-1].append(cell_input + '*')

        self._grid = logic.Grid(board)

    def _add_all_entries(self):
        for row in range(9):
            self._entries.append([])
            self._window.rowconfigure(row, weight=1)
            for col in range(9):
                self._window.columnconfigure(col, weight=1)
                self._entries[-1].append(self._create_text_entry(row, col))

    def _create_text_entry(self, row, col):
        padx1 = 0
        pady1 = 0
        padx2 = 0
        pady2 = 0
        if row == 2 or row == 5:
            pady2 = 5
        if row == 3 or row == 6:
            pady1 = 5
        if col == 2 or col == 5:
            padx2 = 5
        if col == 3 or col == 6:
            padx1 = 5

        entry = tkinter.Entry(master=self._window, width=2, font=_DEFAULT_FONT, justify='center')
        entry.grid(row=row, column=col, padx=(padx1, padx2), pady=(pady1, pady2),
                   sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        return entry


if __name__ == '__main__':
    SudokuInput().run()
