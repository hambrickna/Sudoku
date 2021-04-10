from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, X
import argparse
import random
import copy

BOARDS = ["test"]  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


def generateBoard():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    board3 = copy.deepcopy(board)
    i = 0
    counter = 0
    solvable = True
    while counter < 30:
        solve_Sudoku.counter = 0
        counter = 0
        randRow = random.randint(0, 8)
        randCol = random.randint(0, 8)

        if board[randRow][randCol] == 0:
            possibleNums = possible_nums(board, randRow, randCol)
            if len(possibleNums) > 0:
                randNum = random.choice(possibleNums)
                board2 = copy.deepcopy(board)
                board2[randRow][randCol] = randNum
                board3 = copy.deepcopy(board2)
                # printSudoku(board3)
                if solve_Sudoku(board3):
                    i += 1
                    print(i)
                    board = copy.deepcopy(board2)

        for it in range(9):
            for j in range(9):
                if board[it][j] != 0:
                    counter += 1

    print("number of numbers added: ", i)
    print("counter: ", counter)

    count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                count += 1

    while count < 51:
        count = 0
        board[random.randint(0, 8)][random.randint(0, 8)] = 0
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    count += 1

    f = open("test.sudoku", "w")
    for row in range(9):
        if row != 0:
            f.write("\n")
        for col in range(9):
            f.write(str(board[row][col]))
    f.close()
    f = open("test.sudoku", "r")
    print(f.read())
    f.close()
    with open("test.sudoku", "r") as file:
        newgame = sudokuGame(file)
        newgame.start()
        return newgame


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--board", help="Desired board name", type=str, choices=BOARDS, required=True
    )

    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())
    return args["board"]


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text="Clear answers", command=self.__clear_answers)
        clear_button.pack(fill=X, side=BOTTOM)

        solve_button = Button(self, text="Solve Puzzle", command=self.__solve_puzzle)
        solve_button.pack(fill=X, side=BOTTOM)

        generate_button = Button(
            self, text="Generate New Board", command=self.__generate_board
        )
        generate_button.pack(fill=X, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="green", tags="cursor")

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1, tags="victory", fill="purple", outline="purple"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y, text="You win!", tags="victory", fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE

            # if cell was selected already - deselect it
            row = int(row)
            col = int(col)
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif str(self.game.puzzle[row][col]) in "1234567890":
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win(self.game.puzzle):
                self.__draw_victory()

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()

    def __solve_puzzle(self):
        self.game.start()
        self.game.solve_Sudoku(self.game.puzzle)
        self.__draw_puzzle()

    def __generate_board(self):
        self.game = generateBoard()
        self.__clear_answers()


class SudokuBoard(object):
    """
    Sudoku Board representation
    """

    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board


class sudokuGame(object):
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def printSudoku(self, arr):
        for row in range(9):
            for col in range(9):
                print(arr[row][col], end="")
            print()

    def findBlanks(self, arr, l):
        for row in range(9):
            for col in range(9):
                if arr[row][col] == 0:
                    l[0] = row
                    l[1] = col
                    return True
        return False

    def checkHorizontal(self, arr, row, num):
        for col in range(9):
            if arr[row][col] == num:
                return True
        return False

    def checkVertical(self, arr, col, num):
        for row in range(9):
            if arr[row][col] == num:
                return True
        return False

    def checkBox(self, arr, row, col, num):
        for i in range(3):
            for j in range(3):
                if arr[row + i][col + i] == num:
                    return True
        return False

    def possible_nums(self, arr, row, col):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        col_copy = col
        row_copy = row
        copy = nums
        for i in range(3):
            for j in range(3):
                if arr[(row - row % 3) + i][(col - col % 3) + j] in nums:
                    copy.remove(arr[(row - row % 3) + i][(col - col % 3) + j])

        for row in range(9):
            if arr[row][col_copy] in nums:
                copy.remove(arr[row][col_copy])

        for col in range(9):
            if arr[row_copy][col] in nums:
                copy.remove(arr[row_copy][col])
        return copy

    def checkMoveIsSafe(self, arr, row, col, num):
        return (
            not self.checkHorizontal(arr, row, num)
            and not self.checkVertical(arr, col, num)
            and not self.checkBox(arr, row - row % 3, col - col % 3, num)
        )

    def check_win(self, arr):
        l = [0, 0]
        if not (self.findBlanks(arr, l)):
            print("firstcheck")
            for row in range(9):
                for col in range(9):
                    num = arr[row][col]
                    arr[row][col] = 0
                    if not (self.checkMoveIsSafe(arr, row, col, num)):
                        print("second check")
                        self.printSudoku(arr)
                        return False
                    arr[row][col] = num
        else:
            print("third check")
            return False
        print("fourth check")
        return True

    def solve_Sudoku(self, arr):
        l = [0, 0]
        if not (self.findBlanks(arr, l)):
            return True
        row = l[0]
        col = l[1]
        possibleNums = self.possible_nums(arr, row, col)
        for num in possibleNums:
            if self.checkMoveIsSafe(arr, row, col, num):
                arr[row][col] = num
                self.arr = arr
            if self.solve_Sudoku(arr):
                return True
            arr[row][col] = 0
        return False


def printSudoku(arr):
    for row in range(9):
        for col in range(9):
            print(arr[row][col], end="")
        print()


def solve_Sudoku(arr):
    l = [0, 0]
    solve_Sudoku.counter += 1
    if solve_Sudoku.counter > 300:
        return False

    if not (findBlanks(arr, l)):
        return True
    row = l[0]
    col = l[1]
    if not (checkValidBoard(arr)):
        print("Invalid?")
        return False
    possibleNums = possible_nums(arr, row, col)
    for num in possibleNums:
        if checkMoveIsSafe(arr, row, col, num):
            arr[row][col] = num
        if solve_Sudoku(arr):
            return True
        arr[row][col] = 0
    return False


def checkValidBoard(arr):
    for row in range(9):
        for col in range(9):
            num = arr[row][col]
            if num != 0:
                arr[row][col] = 0
                if not checkMoveIsSafe(arr, row, col, num):
                    print("uhhh")
                    return False
                arr[row][col] = num
    return True


def checkMoveIsSafe(arr, row, col, num):
    return (
        not checkHorizontal(arr, row, num)
        and not checkVertical(arr, col, num)
        and not checkBox(arr, row - row % 3, col - col % 3, num)
    )


def findBlanks(arr, l):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False


def checkHorizontal(arr, row, num):
    for col in range(9):
        if arr[row][col] == num:
            return True
    return False


def checkVertical(arr, col, num):
    for row in range(9):
        if arr[row][col] == num:
            return True
    return False


def checkBox(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if arr[row + i][col + i] == num:
                return True
    return False


def possible_nums(arr, row, col):
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    col_copy = col
    row_copy = row
    for i in range(3):
        for j in range(3):
            if arr[(row - row % 3) + i][(col - col % 3) + j] in nums:
                nums.remove(arr[(row - row % 3) + i][(col - col % 3) + j])

    for row in range(9):
        if arr[row][col_copy] in nums:
            nums.remove(arr[row][col_copy])

    for col in range(9):
        if arr[row_copy][col] in nums:
            nums.remove(arr[row_copy][col])
    return nums


if __name__ == "__main__":
    board_name = parse_arguments()

    random.seed(a=None, version=2)

    with open("%s.sudoku" % board_name, "r") as boards_file:
        game = sudokuGame(boards_file)
        game.start()

        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 140))
        root.mainloop()
