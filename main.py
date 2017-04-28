import pygame, random, sys, time, math
from pygame.locals import *
import ai, reversi
import os

# quit function
def quit():
    pygame.quit()
    sys.exit()

COUNTER_SIZE = 40
TILE_SIZE = 50
COUNTER_PADDING = 5
#refresh speed
FPS = 200

#windows_size
WINDOWWIDTH = TILE_SIZE * 8
WINDOWHEIGHT = TILE_SIZE * 8

class Engine_v1 (object):
    def __init__(self):
        super(Engine_v1, self).__init__()
        self.resources = {}


        #create game
        self.game = reversi.Reversi()

    def startup(self):
        # set up pygame, the window, and the mouse cursor
        pygame.init()
        self.main_clock = pygame.time.Clock()
        # Open a window on the screen with size
        self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Reversi-6364AI-Project')
        # pygame.mouse.set_visible(False)



        # set up images
        self.resources['board'] = pygame.image.load('media/board.png')
        self.resources['black'] = pygame.image.load('media/black.png')
        self.resources['white'] = pygame.image.load('media/white.png')

        self.draw_board()

    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, (0,0,0))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    # after reversi move and change the gameboard, retrieve the data from the board for drawing the UI
    def draw_board(self):
        # create the board
        the_board = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
        #blit() draw one image onto another
        self.surface.blit(self.resources['board'], the_board)

        # set up tile on board
        for x in range(0, 8):
            for y in range(0, 8):
                player = self.game.board[x][y]

                counter = pygame.Rect(x * TILE_SIZE + COUNTER_PADDING, y * TILE_SIZE + COUNTER_PADDING, COUNTER_SIZE, COUNTER_SIZE)

                #different img for two player
                if player == 1:
                    self.surface.blit(self.resources['white'], counter)
                elif player == 2:
                    self.surface.blit(self.resources['black'], counter)

        # Has a victory occurred?
        font = pygame.font.SysFont("Helvetica", 48)
        if self.game.victory == -1:
            self.drawText("Draw", font, self.surface, 95, 10)

        if self.game.victory == 1:
            self.drawText("White Win", font, self.surface, 48, 10)

        if self.game.victory == 2:
            self.drawText("Black Win", font, self.surface, 48, 10)


        #refresh
        pygame.display.update()


    #-event-
    #mouse click
    def handle_mousedown(self, event):
        pass
    #finish mouse click
    def handle_mouseup(self, event):
        #calculate position
        x, y = event.pos
        tx = int(math.floor(x/TILE_SIZE))
        ty = int(math.floor(y/TILE_SIZE))

        try:
            #try process player step
            self.game.player_move(tx, ty)

        except reversi.Illegal_move as e:
            print("Illegal move")
        except Exception as e:
            raise

    def handle_mousemove(self, event):
        pass


    def new_game(self):
        self.game.__init__()

#start function
    def start(self):

        self.startup()
        self.new_game()

        while True:

            for event in pygame.event.get():


                if event.type == MOUSEBUTTONUP:
                    self.handle_mouseup(event)

                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mousedown(event)

                elif event.type == MOUSEMOTION:
                    self.handle_mousemove(event)

               # else:
                #    pass
                    # print(event)

            # only when change happened then update the UI
            if self.game.has_changed:
                self.draw_board()
                self.game.has_changed = False

            if self.game.ai_is_ready:
                self.game.ai_move()

            #control the refresh speed
            self.main_clock.tick(FPS)

        quit()

if __name__ == '__main__':
        ge = Engine_v1()
        ge.start()
