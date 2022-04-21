import random
import sys
import os
import itertools
import copy
import argparse

def rotate_clock(matrix):
    ruota = list(zip(*reversed(matrix)))
    return [list(elemento) for elemento in ruota]


def rotate_counter(matrix):
    ruota = list(zip(*reversed(matrix)))
    return [list(elemento)[::-1] for elemento in ruota][::-1]


def trim(seqs, direction=0):
    """
    [0,2,2,0]
    1. [2,2] # remove 0s
    2. [2,2] + [0,0,0,0] -> [2,2,0,0,0,0] # move left
       [0,0,0,0] + [2,2] -> [0,0,0,0,2,2] # move right
    3. [2,2,0,0,0,0][:4] -> [2,2,0,0]
       [0,0,0,0,2,2][-4:] -> [0,0,2,2]
    :param seqs:
    :param direction:
    :return:
    """
    zeros = [0] * 4
    if direction:
        return (zeros + [n for n in seqs if n])[-4:]  # move right
    else:
        return ([n for n in seqs if n] + zeros)[:4]  # dir == 0, move left


def sum_seqs(seqs, direction=0):
    """
    [0,1] [1,2] [2,3]
    :param seqs:
    :param direction:
    :return:
    """
    if direction:
        if seqs[2] and seqs[3] and seqs[2] == seqs[3]:  # 2 3 are the same
            seqs[2], seqs[3] = seqs[2] * 2, 0
        if seqs[1] and seqs[2] and seqs[1] == seqs[2]:
            seqs[1], seqs[2] = seqs[1] * 2, 0
        if seqs[0] and seqs[1] and seqs[0] == seqs[1]:  # 0 1 are the same
            seqs[0], seqs[1] = seqs[0] * 2, 0
    else:
        if seqs[0] and seqs[1] and seqs[0] == seqs[1]:  # 0 1 are the same
            seqs[0], seqs[1] = seqs[0] * 2, 0
        if seqs[1] and seqs[2] and seqs[1] == seqs[2]:
            seqs[1], seqs[2] = seqs[1] * 2, 0
        if seqs[2] and seqs[3] and seqs[2] == seqs[3]:  # 2 3 are the same
            seqs[2], seqs[3] = seqs[2] * 2, 0

    return trim(seqs, direction=direction)


def up(board):
    board_rotated = rotate_counter(board)
    return rotate_clock(left(board_rotated))


def down(board):
    board_rotated = rotate_clock(board)
    return rotate_counter(left(board_rotated))


def left(board):
    return [sum_seqs(trim(row)) for row in board]


def right(board):
    return [sum_seqs(trim(row, direction=1), direction=1) for row in board]


class Game:

    def __init__(self):
        self.board = [[0] * 4 for i in range(0, 4)]
        self.controls = ['w', 's', 'a', 'd']

    def get_available_moves(self):
        available_move=[]
        for control in self.controls:
            board = {'w': up, 's': down, 'a': left, 'd': right}[control](
            copy.deepcopy(self.board))  # loop thorough the control options
            if board != self.board:  # test if moved, if true, it's an available move
                available_move.append(control)
        return available_move

    def rnd_field(self):
        number = random.choice([4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2])
        x, y = random.choice(
            [(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.board[x][y] == 0])
        self.board[x][y] = number

    def rnd_field_withreturn(self):
        number = random.choice([4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2])
        x, y = random.choice(
            [(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.board[x][y] == 0])
        self.board[x][y] = number
        return number

    def print_screen(self):
        os.system('clear')
        print('-' * 21)
        # print(self.board)
        for row in self.board:
            print('|{}|'.format("|".join([str(col or ' ').center(4) for col in row])))
            print('-' * 21)

    def logic(self, control, spawn=1):
        board = {'w': up, 'a': left, 's': down, 'd': right}[control](
            copy.deepcopy(self.board))  # pass board into moving function and get a new board
        if board != self.board:  # test if moved
            del self.board[:]  # delete the old board
            self.board.extend(board)  # replace the board with the new one
            if [i for i in itertools.chain(*board) if i >= 2048]:
                return 1, "You Win!"
            if spawn:
                self.rnd_field()  # after movement, generate a new 2/4 at random position
        else:  # if nothing changed
            print("nothing changed")
            if not [1 for g in [f(board) for f in [up, down, left, right]] if
                    g != self.board]:  # can't move in four directions
                return -1, "You Lost"

        return 0, ''  # 1, "You win" -1 "You Lost"

    def main_loop(self):
        self.board = [[0] * 4 for i in range(0, 4)]
        self.rnd_field()
        self.rnd_field()
        while True:
            self.print_screen()
            control = input('input w/a/s/d: ')
            if control in self.controls:
                status, info = self.logic(control)
                if status:
                    print(info)
                    if input('Start another game?[Y/n]').lower() == 'y':
                        break
                    else:
                        sys.exit(0)
        self.main_loop()

    def testboard(self):
        self.board = [[2, 16, 4, 0],
                      [4, 8, 6, 2],
                      [9, 3, 8, 4],
                      [5, 7, 6, 7]]
        board_save = self.board[:]
        possible_boards = []
        while True:
            self.print_screen()
            available_moves = self.get_available_moves() # ACTION(s): set of legal moves
            print('availabe moves:', available_moves)
            for control in available_moves:
                self.board = board_save.copy() # state s
                print('The control is ', control)
                status, info =  self.logic(control)
                possible_boards = self.board
                print(*possible_boards, sep='\n')
            control = input('input w/a/s/d: ')


if __name__ == '__main__':
    Game().main_loop() # uncomment this to play the game
    # Game().testboard() # this runs the test function, not the full game

######################################
########### self test zone  ##########
######################################

# board = [[0] * 4 for i in range(0, 4)]
# board = [[1,2,3],[1,2,4],[1,2,4]]
# size = len(board)

# for row in board:
#     print('|{}|'.format("|".join([str(col or ' ').center(4) for col in row])))
#     print('-' * 21)

# board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
# x, y = random.choice([(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if board[x][y] == 0])
# print(x,y)

# dictionary with functions
# def funca():
#     print("this is a")
#     return 1
#
#
# def funcb():
#     print("this is b")
#     return 2


# testdic = {'a': funca, 'b': funcb}['a']()
# print((testdic))

# deep copy
# a = {1: [1, 2, 3]}
# b = a.copy()
# c = copy.deepcopy(a)
# a[1].append(4)
# print('a', a)
# print('b', b)
# print('c', c)

# list extend
# testlist = [[1, 1, 1], [2, 2, 2]]
# # print(testlist)
# extendlist = [[3, 3, 3], [4, 4, 4]]
# del testlist[:]
# testlist.extend(extendlist)
# testlist = extendlist
# print(testlist)

# itertools.chain()
testlist = [[2, 2, 4, 4],
            [4, 8, 6, 2],
            [4, 8, 0, 4],
            [4, 12, 6, 16]]
## my version
# for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]):
#     if testlist[x][y] == 16:
#         print('found 16 at', x,y)
#         break
#     if (x,y) == (3,3):
#         print('Not found')
## his version
# print(testlist)
# if [i for i in itertools.chain(*testlist) if i >= 16]:
#     print('win')
# else:
#     print('lose')

## trim
# n = 7
# n = [n if n > 5 else n - 1]
# print(n)
# print(testlist[1][:2])
# seqs = testlist[0]
# print(*testlist, sep='\n')
# print('')
# newlist = [sum_seqs(row) for row in testlist]
# print(*newlist, sep='\n')
# print('')
# newlist = [sum_seqs(trim(row)) for row in testlist]
# print(*newlist, sep='\n')

#### move test #####
# print(*testlist,sep='\n')
# print('')
# rotate = rotate_counter(testlist)
# print(*rotate,sep='\n')
# print('')
# rotate = up(testlist)
# print(*rotate,sep='\n')
#### move test #####
# print(*testlist,sep='\n')
# print(' ')
# res = right(testlist)
# print(*res,sep='\n')
