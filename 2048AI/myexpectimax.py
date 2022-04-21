import copy

from GAMECOPY import Board

AVAILABLE_MOVES = ['w', 's', 'a', 'd']

def utility(self, game: Board):
    return self.heuristic_val(game)


def expectimax(self, game: Board, width: int, root: int = 0):  # root == 1, terminal test;
    if root:
        hVal = self.utility(game)
        return hVal

    # default self.player == True
    if self.player:  # find max for all possible actions
        available_moves = game.get_available_moves()  # available_moves = e.g. ['w','a','s']
        chance_list = [0] * len(
            available_moves)  # initial the list containing the eval for different moves ## can be optimized as chance_list.append()
        for idx in range(len(available_moves)):
            child_board = copy.deepcopy(game)  # deep copy of the origin board
            child_board.move_manager(available_moves[idx])
            self.player = False  # turn to CHANCE
            chance_list[idx] = self.expectimax(child_board, width, 0)
            # self.dir = # choose the best action
        max_index = chance_list.index(max(chance_list))  # find the max eval index in chancelist
        dir = available_moves[max_index]  # get the best move in available_moves based on the index of the max eval
        return dir
    else:  # sum of probability
        # 'game' here is 'child_board'
        chance_eval = 0
        potentials = game.free_tiles()
        num_potentials = len(potentials)  # gives the amount of possible grandboards
        for i in range(num_potentials):  # try 'width' possible grandchild boards
            grandchild_board = copy.deepcopy(game)  # copy child to grandchild
            spawn_num = grandchild_board.spawn_with_return()  # generate new board and return the spawn_num;
            # should be optimized to make different spawms(now has potential to make same guess)
            if spawn_num == 2:
                utility_p = 0.9 * self.expectimax(grandchild_board, width, 1) * 1 / num_potentials
            else:
                utility_p = 0.1 * self.expectimax(grandchild_board, width, 1) * 1 / num_potentials
            chance_eval += utility_p  # sum up the chances

        return chance_eval