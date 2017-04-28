import ai

class Game_error(Exception):
    """Errors related to the game in general"""
    pass

class Illegal_move(Game_error):
    """Errors from illegal moves"""
    pass

#class Game_rule_error(Game_error):
 #   """Errors that arise from rule issues"""
  #  pass




class Reversi (object):

	
    def __init__(self):
        super(Reversi, self).__init__()
        
        self.turn = 1
        self.player = 1
        self.victory = 0

        #set up board data

        """
            0 = Empty
            1 = White
            2 = Black
        """
        self.board = [[0 for x in range(8)] for x in range(8)]

        #initialize board data,put piece in it
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1

        # Setup AI
        self.ai = ai.Game_ai(self)
        
        self.has_changed = True
        self.ai_is_ready = False
    
    def player_move(self, x, y):
        #check game situation
        if self.victory != 0:
            return
        
        # Now is it turn to AI or player?
        if self.player != 1:
            return
        # process the move which player choosed
        self.perform_move(x,y)
    #   boardprint = map(list, zip(*self.board))
    #   for i in range(0,8):
    #      print boardprint[i][:]
        # Maybe have the AI make a move
        self.ai_is_ready = True
    
    def perform_move(self, x, y):
        # check that the tile is empty or already has the piece
        # if tile already has a piece in here ,then cannot be placed a new one.
        if self.board[x][y] != 0:


            raise Illegal_move("occupied by other".format(
                self.player,
                x, y,
                self.board[x][y]
            ))

        
        # Place it and work out the flips
        self.place_piece(x, y)
        
        # after place piece ,check the game is end or not.
        all_tiles = [item for sublist in self.board for item in sublist]
        
        empty_tiles = sum(1 for tile in all_tiles if tile == 0)
        white_tiles = sum(1 for tile in all_tiles if tile == 1)
        black_tiles = sum(1 for tile in all_tiles if tile == 2)
        
        # No moves left to make, end the game
        if white_tiles < 1 or black_tiles < 1 or empty_tiles < 1:
            self.end_game()
            return
        
        # check movable possibility
        if self.player == 1:
            move_found = self.move_can_be_made()
        else:
            move_found = True
        if not move_found:
            self.end_game()
            return

        #game continue
        # Alternate between player 1 and 2

        self.player = 3 - self.player
        self.has_changed = True

    #try every situation, to check still have movable steps.
    def move_can_be_made(self):
        move_found = False
        #traverse all board
        for x in range(0,8):
            for y in range(0,8):
                if move_found: continue
                if self.board[x][y] == 0:
                    c = self.place_piece(x, y, live_mode=False)
                    if c > 0:
                        move_found = True
        
        return move_found


    def ai_move(self):
        # go to ai.py to perform ai decision.
        self.ai.make_move()
        self.ai_is_ready = False

    # end_game , output result.
    def end_game(self):
        all_tiles = [item for sublist in self.board for item in sublist]
        
        white_tiles = sum(1 for tile in all_tiles if tile == 1)
        black_tiles = sum(1 for tile in all_tiles if tile == 2)
        
        if white_tiles > black_tiles:
            self.victory = 1
        elif white_tiles < black_tiles:
            self.victory = 2
        else:
            self.victory = -1
        
        self.has_changed = True

    # place the piece on the board
    def place_piece(self, x, y, live_mode=True):

        #player place the piece
        if live_mode:
            self.board[x][y] = self.player


        change_count = 0
        
        # create reference to the row and column that player just placed a piece on
        # a crossroad with (column,row )
        column = self.board[x]
        row = [self.board[i][y] for i in range(0,8)]

        # <<<< Reverse Rule>>>>

        # up direction
        if self.player in column[:y]:
            changes = []
            search_complete = False

            #search pieces that can be reverse
            for i in range(y-1,-1,-1):
                if search_complete: continue
                
                counter = column[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[x][i] = self.player
        
        # Down
        if self.player in column[y:]:
            changes = []
            search_complete = False
            
            for i in range(y+1,8,1):
                if search_complete: continue
                
                counter = column[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[x][i] = self.player
        
        # Left
        if self.player in row[:x]:
            changes = []
            search_complete = False
            
            for i in range(x-1,-1,-1):
                if search_complete: continue
                
                counter = row[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[i][y] = self.player
        
        # Right
        if self.player in row[x:]:
            changes = []
            search_complete = False
            
            for i in range(x+1,8,1):
                if search_complete: continue
                
                counter = row[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[i][y] = self.player
        
        # Diagonals detect
        i, j = x-7, y+7
        bl_tr_diagonal = []
        
        for q in range(0, 16):
            if 0 <= i < 8 and 0 <= j < 8:
                bl_tr_diagonal.append(self.board[i][j])
            
            i += 1
            j -= 1
        
        i, j = x-7, y-7
        br_tl_diagonal = []
        for q in range(0, 16):
            
            if 0 <= i < 8 and 0 <= j < 8:
                br_tl_diagonal.append(self.board[i][j])
            
            i += 1
            j += 1
        
        # Up Right
        if self.player in bl_tr_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx += 1
                ly -= 1
                
                if lx > 7 or ly < 0: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        # Down Left
        if self.player in bl_tr_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx -= 1
                ly += 1
                
                if lx < 0 or ly > 7: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                
                if counter == 0:
                    changes = []
                    search_complete = True
                    break
                elif counter == self.player:
                    search_complete = True
                    break
                else:
                    changes.append((lx, ly))
            
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        
        # Up Left
        if self.player in br_tl_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx -= 1
                ly -= 1
                
                if lx < 0 or ly < 0: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        # Down Right
        if self.player in br_tl_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx += 1
                ly += 1
                
                if lx > 7 or ly > 7: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player

        # no change happend situation.
        if change_count == 0 and live_mode:


            self.board[x][y] = 0
            raise Illegal_move("no flips!! ".format(
                self.player,
                x, y,
            ))


        return change_count

    
