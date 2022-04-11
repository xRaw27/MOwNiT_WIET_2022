import numpy as np


class Sudoku:
    def __init__(self, init_board_path):
        self.path = init_board_path
        self.init_board = None
        self.empty = None
        self.read_from_file()
        self.board = None
        self.random_init_state()

    def read_from_file(self):
        init_board = [[] for _ in range(9)]
        empty = [[] for _ in range(9)]
        with open(self.path) as f:
            init_board_text = f.read()
            for i, field in enumerate(init_board_text):
                if field == "x":
                    init_board[(i // 27) * 3 + (i % 9) // 3].append(0)
                    empty[(i // 27) * 3 + (i % 9) // 3].append(((i // 9) % 3) * 3 + (i % 9) % 3)
                else:
                    init_board[(i // 27) * 3 + (i % 9) // 3].append(int(field))

        self.init_board = np.array(init_board)
        self.empty = empty

    def random_init_state(self):
        self.board = self.init_board.copy()
        for i in range(9):
            square = self.board[i, :]
            not_included = set(range(10))
            not_included.remove(0)
            for x in square:
                if x != 0:
                    not_included.remove(x)

            rand = np.random.permutation(list(not_included))
            j = 0
            for k in range(9):
                if square[k] == 0:
                    square[k] = rand[j]
                    j += 1

    def make_move(self, mv):
        square, a, b = mv
        self.board[square, a], self.board[square, b] = self.board[square, b], self.board[square, a]

    def random_move(self):
        square = np.random.randint(0, 9)
        while len(self.empty[square]) < 2:
            square = np.random.randint(0, 9)

        a, b = np.random.choice(self.empty[square], 2, replace=False)

        self.board[square, a], self.board[square, b] = self.board[square, b], self.board[square, a]
        new_cost = self.cost()
        self.board[square, a], self.board[square, b] = self.board[square, b], self.board[square, a]

        return new_cost, (square, a, b)

    def get_state(self):
        return self.board.copy()

    def cost(self):
        cost_sum = 0

        for idx in range(9):
            count = np.zeros(10, int)

            square = 3 * (idx // 3)
            start = 3 * (idx % 3)
            stop = start + 3
            for i in range(square, square + 3):
                for j in range(start, stop):
                    x = self.board[i, j]
                    count[x] += 1
                    if count[x] > 1:
                        cost_sum += 1

            count = np.zeros(10, int)
            square = idx // 3
            start = idx % 3
            for i in range(square, 9, 3):
                for j in range(start, 9, 3):
                    x = self.board[i, j]
                    count[x] += 1
                    if count[x] > 1:
                        cost_sum += 1

        return cost_sum

    def plot(self, board=None):
        if board is not None:
            self.board = board
        print(self)

    def empty_cells(self):
        res = 0
        for square in self.empty:
            res += len(square)
        return res

    def __repr__(self):
        return f"Sudoku: \n  init_board:\n{self.init_board}\n  board:\n{self.board}\n  empty: \n{self.empty}"

    def __str__(self):
        res = f"Empty cells = {self.empty_cells()}\nCost = {self.cost()}\nSolution:\n"
        for row in range(9):
            res += " "
            for col in range(9):
                idx1 = (row // 3) * 3 + col // 3
                idx2 = (row % 3) * 3 + col % 3
                res += str(self.board[idx1, idx2])
                if col in (2, 5):
                    res += " | "
            res += "\n"
            if row in (2, 5):
                res += "-----|-----|-----\n"

        return res
