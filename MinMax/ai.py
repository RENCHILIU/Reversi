import time
import os, copy


minEvalBoard = -1  # min - 1
maxEvalBoard = 8 * 8 + 4 * 8 + 4 + 1  # max + 1

class Game_ai(object):
    def __init__(self, game):
        super(Game_ai, self).__init__()
        self.game = game
        self.move = (-1, -1)

  def make_move(self):
        x,y = self.BestMove(self.game.board)
        if x == -1 and y == -1:
            print '-1'
            self.game.end_game()
        else:
            self.game.perform_move(x, y)
            move_found = self.game.move_can_be_made()
            if not move_found:
                self.game.end_game()
                return

        boardprint = map(list, zip(*self.game.board))
        print '----------'
        for i in range(0, 8):
            print boardprint[i][:]
        print '----------'


    def BestMove(self,board):
        maxPoints = -1
        mx = 7
        my = 7
        for y in range(8):
            for x in range(8):
                if self.ValidMove(board, x, y):
                    (boardTemp, reverse_num) = self.MakeMove(copy.deepcopy(board), x, y)
                    points = self.Minimax(boardTemp, 3, True)

                    if points > maxPoints:
                        maxPoints = points
                        mx = x
                        my = y
        return (mx, my)

    def MakeMove(self,board, x, y):  # try,assuming valid move
        reverse_num = self.game.place_piece(x, y, False)
        boardTemp = copy.deepcopy(board)
        boardTemp[x][y] = 2
        return (boardTemp, reverse_num)

    def Minimax(self, board, depth, maximizingPlayer):
        if depth == 0 or self.IsTerminalNode(board):
            return self.EvalBoard(board)

        if maximizingPlayer:
            bestValue = minEvalBoard
            for y in range(8):
                for x in range(8):
                    if self.ValidMove(board, x, y):
                        (boardTemp, reverse_num) = self.MakeMove(copy.deepcopy(board), x, y)
                        v = self.Minimax(boardTemp, depth - 1, False)
                        bestValue = max(bestValue, v)
        else:  # minimizingPlayer
            bestValue = maxEvalBoard
            for y in range(8):
                for x in range(8):
                    if self.ValidMove(board, x, y):
                        (boardTemp, reverse_num) = self.MakeMove(copy.deepcopy(board), x, y)
                        v = self.Minimax(boardTemp, depth - 1, True)
                        bestValue = min(bestValue, v)

        return bestValue


    # valid steps
    def ValidMove(self,board, x, y):
        if board[x][y] != 0:
            return False
        boardTemp = copy.deepcopy(board)
        (boardTemp, reverse_num) = self.MakeMove(boardTemp, x, y)

        #if no reverse ,then is not true.
        if reverse_num == 0:
            return False
        return True

    def EvalBoard(self,board):
        tot = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 2:
                    if (x == 0 or x == 8 - 1) and (y == 0 or y == 8 - 1):
                        tot += 4  # corner
                    elif (x == 0 or x == 8 - 1) or (y == 0 or y == 8 - 1):
                        tot += 2  # side
                    else:
                        tot += 1
        return tot

    def IsTerminalNode(self,board):
        for y in range(8):
            for x in range(8):
                if self.ValidMove(board, x, y):
                    return False
        return True
