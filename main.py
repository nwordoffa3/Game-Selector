from tkinter.messagebox import QUESTION
from turtle import Screen
from button import Button

import pygame, sys, random
import numpy as np


pygame.init()

#helpful variables
WIDTH, HEIGHT = 860, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0, 0)
GREEN = (0,255,0)

#screen setup
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game Selector")
backGround = pygame.image.load("assets/8bitbackground.jpg")
backGround = pygame.transform.scale(backGround, (WIDTH, HEIGHT))

def font(size):
        return pygame.font.Font("assets/font.ttf", size)

def pong():
    pygame.display.set_caption("Pong")

    FPS = 60

    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    BALL_RADIUS = 7

    SCORE_FONT = font(50)
    WINNING_SCORE = 6
    
    class Paddle:
        COLOR = WHITE
        VEL = 4

        def __init__(self, x, y, width, height):
            self.width = width
            self.height = height
            self.x = self.original_x = x
            self.y = self.original_y = y
            

        def draw(self, window):
            pygame.draw.rect(
                window, self.COLOR, (self.x, self.y, self.width, self.height))

        def move(self, up=True):
            if up:
                self.y -= self.VEL
            else:
                self.y += self.VEL

        def reset(self):
            self.x = self.original_x
            self.y = self.original_y
    class Ball:
        MAX_VEL = 5
        COLOR = WHITE

        def __init__(self, x, y, radius):
            self.radius = radius
            self.x_vel = self.MAX_VEL
            self.y_vel = 0
            
            self.x = self.original_x = x
            self.y = self.original_y = y
            

        def draw(self, window):
            pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

        def move(self):
            self.x += self.x_vel
            self.y += self.y_vel

        def reset(self):
            if self.x < 0 : 
                self.x_vel = self.MAX_VEL
            else:
                self.x_vel = -1*self.MAX_VEL
            self.x = self.original_x
            self.y = self.original_y
            self.y_vel = 0

    def draw(window, paddles, ball, left_score, right_score):
        window.fill(BLACK)

        left_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
        right_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
        window.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
        window.blit(right_text, (WIDTH * (3/4) -
                                    right_text.get_width()//2, 20))

        for paddle in paddles:
            paddle.draw(window)

        for i in range(10, HEIGHT, HEIGHT//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

        ball.draw(window)
        pygame.display.update()

    def handle_collision(ball, left_paddle, right_paddle):
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1.1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1.1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1.1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1.1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

    def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)  

    def main():
        run = True
        time = pygame.time.Clock()

        left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                            2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                            2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

        left_score = 0
        right_score = 0

        while run:
            time.tick(FPS)
            draw(SCREEN, [left_paddle, right_paddle], ball, left_score, right_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle)

            if ball.x < 0:
                right_score += 1
                ball.reset()
            elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

            won = False
            
            if left_score >= WINNING_SCORE:
                won = True
                win_text = "Left Player Won!"
            elif right_score >= WINNING_SCORE:
                won = True
                win_text = "Right Player Won!"

            if won:
                text = SCORE_FONT.render(win_text, 1, WHITE)
                SCREEN.blit(text, (WIDTH//2 - text.get_width() //
                                2, HEIGHT//2 - text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(5000)
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                left_score = 0
                right_score = 0

        pygame.quit()

    if __name__ == '__main__':
        main()

def snake():
    pygame.display.set_caption( 'Snek' )
    
    up = (0,-1)
    down = (0,1)
    left = (-1,0)
    right = (1,0)
    
    gridSize = 20
    grid_width = WIDTH/gridSize
    grid_height = HEIGHT/gridSize


    class Snake():
        def __init__(self):
            self.length = 1
            self.positions = [((420), (HEIGHT/2))]
            self.direction = random.choice([up, down, left, right])
            self.color = (0,255,0)
            self.score = 0

        def get_head_position(self):
            return self.positions[0]

        def turn(self, point):
            if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
                return
            else:
                self.direction = point

        def move(self):
            pos = self.get_head_position()
            x,y = self.direction
            new = (((pos[0]+(x*gridSize))%WIDTH), (pos[1]+(y*gridSize))%HEIGHT)
            if len(self.positions) > 2 and new in self.positions[2:]:
                self.reset()
            else:
                self.positions.insert(0,new)
                if len(self.positions) > self.length:
                    self.positions.pop()

        def reset(self):
            self.length = 1
            self.positions = [((420), (HEIGHT/2))]
            self.direction = random.choice([up, down, left, right])
            self.score = 0

        def draw(self,surface):
            for p in self.positions:
                r = pygame.Rect((p[0], p[1]), (gridSize,gridSize))
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, (93,216, 228), r, 1)

        def handle_keys(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.turn(up)
                    elif event.key == pygame.K_DOWN:
                        self.turn(down)
                    elif event.key == pygame.K_LEFT:
                        self.turn(left)
                    elif event.key == pygame.K_RIGHT:
                        self.turn(right)
  
    class Food():
        def __init__(self):
            self.position = (0,0)
            self.color = RED
            self.randomize_position()

        def randomize_position(self):
            self.position = (random.randint(0, grid_width-1)*gridSize, random.randint(0, grid_height-1)*gridSize)

        def draw(self, surface):
            r = pygame.Rect((self.position[0], self.position[1]), (gridSize, gridSize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def drawGrid(surface):
        for col in range(0, int(grid_height)):
            for row in range(0, int(grid_width)):
                    r = pygame.Rect((row*gridSize, col*gridSize), (gridSize,gridSize))
                    pygame.draw.rect(surface,(0,0,0), r)
                
    def main():
        clock = pygame.time.Clock()

        surface = pygame.Surface(SCREEN.get_size())
        surface = surface.convert()
        drawGrid(surface)

        snake = Snake()
        food = Food()

        myfont = font(16)

        while (True):
            clock.tick(10)
            snake.handle_keys()
            drawGrid(surface)
            snake.move()
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
            snake.draw(surface)
            food.draw(surface)
            SCREEN.blit(surface, (0,0))
            text = myfont.render("Score {0}".format(snake.score), 1, WHITE)
            SCREEN.blit(text, (5,10))
            pygame.display.update()

    if __name__ == '__main__':
        main()

def tictactoe():
    pygame.display.set_caption( 'TIC TAC TOE' )
    
    WIDTH, HEIGHT = 600, 600
    LINE_WIDTH, WIN_LINE_WIDTH = 10, 10
    BOARD_ROWS, BOARD_COLS  = 3, 3
    SQUARE_SIZE = 200
    circle = pygame. transform. scale(pygame.image.load("assets/circle.png"), (150, 150))
    x = pygame.transform.scale(pygame.image.load("assets/x.png"), (175,175))

    
    BG_COLOR = (0,0,0)
    LINE_COLOR = (255,255,255)
    
    game = np.zeros( (BOARD_ROWS, BOARD_COLS) )
    SCREEN = pygame.display.set_mode( (WIDTH, HEIGHT) )


    def draw_lines():
        SCREEN.fill('black')
        
        pygame.draw.line( SCREEN, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
        pygame.draw.line( SCREEN, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )

        pygame.draw.line( SCREEN, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
        pygame.draw.line( SCREEN, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )
    
    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if game[row][col] == 2:
                    SCREEN.blit(x, (int( col * SQUARE_SIZE + SQUARE_SIZE//16), int( row * SQUARE_SIZE + SQUARE_SIZE//16)))
                elif game[row][col] == 1:
                    SCREEN.blit(circle, (int( col * SQUARE_SIZE + SQUARE_SIZE//9), int( row * SQUARE_SIZE + SQUARE_SIZE//9)))

    def mark_square(row, col, player):
        game[row][col] = player

    def available_square(row, col):
        return game[row][col] == 0

    def is_game_full():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if game[row][col] == 0:
                    return False

        return True
    def check_win(player):
        for col in range(BOARD_COLS):
            if game[0][col] == player and game[1][col] == player and game[2][col] == player:
                draw_vertical_winning_line(col, player)
                return True

        for row in range(BOARD_ROWS):
            if game[row][0] == player and game[row][1] == player and game[row][2] == player:
                draw_horizontal_winning_line(row, player)
                return True

        if game[2][0] == player and game[1][1] == player and game[0][2] == player:
            draw_asc_diagonal(player)
            return True

        if game[0][0] == player and game[1][1] == player and game[2][2] == player:
            draw_desc_diagonal(player)
            return True

        return False

    def draw_vertical_winning_line(col, player):
        xPos = col * SQUARE_SIZE + SQUARE_SIZE//2

        color = (255, 255, 255) 

        pygame.draw.line( SCREEN, color, (xPos, 15), (xPos, HEIGHT - 15), LINE_WIDTH )

    def draw_horizontal_winning_line(row, player):
        yPos = row * SQUARE_SIZE + SQUARE_SIZE//2

        color = (255, 255, 255) 

        pygame.draw.line( SCREEN, color, (15, yPos), (WIDTH - 15, yPos), WIN_LINE_WIDTH )

    def draw_asc_diagonal(player):
        color = (255, 255, 255) 

        pygame.draw.line( SCREEN, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

    def draw_desc_diagonal(player):
        color = (255, 255, 255) 

        pygame.draw.line( SCREEN, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

    def restart():
        SCREEN.fill( BG_COLOR )
        draw_lines()
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                game[row][col] = 0

    draw_lines()

    player = 1
    game_over = False

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square( clicked_row, clicked_col ):

                    mark_square( clicked_row, clicked_col, player )
                    if check_win( player ):
                        game_over = True
                    player = player % 2 + 1

                    draw_figures()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    player = 1
                    game_over = False

        pygame.display.update()    
    
def hangman():
    
    button_font = font(20)
    guessing_font = font(24)
    lost_font = font(15)
    word = ''
    
    buttons = []
    guessed = []
    hangmanPics = [pygame.image.load('Hangman\images\hangman0.png'), pygame.image.load('Hangman\images\hangman1.png'), pygame.image.load('Hangman\images\hangman2.png'), pygame.image.load('Hangman\images\hangman3.png'), pygame.image.load('Hangman\images\hangman4.png'), pygame.image.load('Hangman\images\hangman5.png'), pygame.image.load('Hangman\images\hangman6.png')]

    limbs = 0
    
    def redraw_game_window():
        SCREEN.fill(BLACK)

        for i in range(len(buttons)):
            if buttons[i][4]:
                
                label = button_font.render(chr(buttons[i][5]), 1, WHITE)

                SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/lettercirc.png"), (35,35)), (buttons[i][1] - (label.get_width() - 15), buttons[i][2] - (label.get_height())))
                SCREEN.blit(label, (buttons[i][1] - (label.get_width() / 2 - 15), buttons[i][2] - (label.get_height() / 2)))

        spacedwrd = spacedOut(word, guessed)
        label = guessing_font.render(spacedwrd, 1, WHITE)
        rect = label.get_rect()
        length = rect[2]
        


        hangmanPic = hangmanPics[limbs]
        SCREEN.blit(label,(WIDTH/2 - length/2 + 100, 20 + hangmanPic.get_height()))
        SCREEN.blit(hangmanPic, (WIDTH/2 - hangmanPic.get_width()/2 - 70, 100))
        pygame.display.update()


    def randomWord():
        file = open('Hangman\words.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)

        return f[i][:-1]


    def hang(guess):
  
        if guess.lower() not in word.lower():
            return True
        else:
            return False


    def spacedOut(word, guessed=[]):
        spacedWord = ''
        guessedLetters = guessed
        for x in range(len(word)):
            if word[x] != ' ':
                spacedWord += '_ '
                for i in range(len(guessedLetters)):
                    if word[x].upper() == guessedLetters[i]:
                        spacedWord = spacedWord[:-2]
                        spacedWord += word[x].upper() + ' '
            elif word[x] == ' ':
                spacedWord += ' '
            
        return spacedWord
                

    def buttonHit(x, y):
        for i in range(len(buttons)):
            if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
                if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                    return buttons[i][5]
        return None


    def end(winner=False):
        lostTxt = 'You Lost :( press any key to play again'
        winTxt = 'WINNER! press any key to play again!'
        redraw_game_window()
        pygame.time.delay(1000)
        SCREEN.fill(BLACK)

        if winner == True:
            label = lost_font.render(winTxt, 1, WHITE)
        else:
            label = lost_font.render(lostTxt, 1, WHITE)

        wordTxt = lost_font.render(word.upper(), 1, BLACK)
        wordWas = lost_font.render('The word was: ', 1, BLACK)

        SCREEN.blit(wordTxt, (WIDTH/2 - wordTxt.get_width()/2, 295))
        SCREEN.blit(wordWas, (WIDTH/2 - wordWas.get_width()/2, 245))
        SCREEN.blit(label, (WIDTH / 2 - label.get_width() / 2, 140))
        pygame.display.update()
        again = True
        while again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    again = False
        reset()


    def reset():

        for i in range(len(buttons)):
            buttons[i][4] = True

        limbs = 0
        guessed = []
        word = randomWord()


    increase = round(WIDTH / 13)
    for i in range(26):
        if i < 13:
            y = 40
            x = 25 + i * increase
        else:
            x = 25 + increase * (i - 13)
            y = 85
        buttons.append([BLACK, x, y, 20, True, 65 + i])

    word = randomWord()
    inPlay = True

    while inPlay:
        redraw_game_window()
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter != None:
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if hang(chr(letter)):
                        if limbs != 5:
                            limbs += 1
                        else:
                            end()
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            end(True)

    pygame.quit()

    

def main_menu():
    while True:
        SCREEN.blit(backGround, (0,0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = font(50).render("WELCOME!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(440, 50))
        
        butt = pygame.image.load("assets/button.png")
        butt = pygame.transform.scale(butt, (260, 90))
        credit = pygame.transform.scale(butt, (100, 50))
        
        PONG_BUTTON = Button(image=butt, pos=(425, 135), 
                            text_input="PONG", font=font(25), base_color="#d7fcd4", hovering_color="White")
        SNAKE_BUTTON = Button(image=butt, pos=(425, 235), 
                            text_input="SNAKE", font=font(25), base_color="#d7fcd4", hovering_color="White")
        HANGMAN_BUTTON = Button(image=butt, pos=(425, 335), 
                            text_input="HANGMAN", font=font(25), base_color="#d7fcd4", hovering_color="White")
        TICTACTOE_BUTTON = Button(image=butt, pos=(425, 435), 
                            text_input="TICTACTOE", font=font(25), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PONG_BUTTON, SNAKE_BUTTON, HANGMAN_BUTTON, TICTACTOE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PONG_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pong()
                if SNAKE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    snake()    
                if TICTACTOE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    tictactoe()
                if HANGMAN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    hangman()    
               
                
        pygame.display.update()
        


main_menu()