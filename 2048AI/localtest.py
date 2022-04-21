import itertools
import random

CHANCE_OF_FOUR = 90

AVAILABLE_MOVES = ['w', 's', 'a', 'd']
board = [[2, 0, 4, 0],
         [4, 8, 6, 2],
         [4, 0, 0, 4],
         [0, 0, 6, 0]]

def rnd_field(board):
    spawn_num = random.randint(1, 100)
    if spawn_num < CHANCE_OF_FOUR:
        number = 2
    else:
        number = 4
    x, y = random.choice(
        [(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if board[x][y] == 0])
    board[x][y] = number
    print(*board,sep='\n')
    return number

# spawm_num = rnd_field(board)
# print(spawm_num)

# for idx in range(len(AVAILABLE_MOVES)):
#     print(idx)
#     print(AVAILABLE_MOVES[idx])


# dirs = [UP, DOWN, LEFT, RIGHT] = range(4)
# for d in dirs:
#     print(d)

controls = ['w', 's', 'a', 'd']
# available_control = []
# for control in controls:
#     if control > 'c':
#         available_control.append(control)
# print(available_control)
copycontrol = controls.copy()
controls.append('wt')
# print(controls)
# print(copycontrol)
available_control = ['w','s','a']
chancelist=[0]*len(available_control)
for idx in range(len(available_control)):
    chancelist[idx] = random.randint(-5,10)
max_index = chancelist.index(max(chancelist))
print(available_control)
print(chancelist)
print(controls[max_index])

