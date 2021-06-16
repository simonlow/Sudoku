import random
import pygame
import math

gameboard = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]];

playing_board = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]];
blanks = 50
wrongs = 0
run = False
screen = pygame.display.set_mode([720, 780])

pygame.font.init()
val_font = pygame.font.SysFont("Arial", 50)
message_font = pygame.font.SysFont("Arial", 50)
curr_x=0
curr_y=0
val=0
def create_board():
    # print_board()
    # print("\n")
    row = 0
    col = 0
    while row < 9:
        while col < 9:
            gameboard[row][col] = random.randint(1, 9)
            if check_possible(row, col):
                while check_equality(row, col):
                    gameboard[row][col] = random.randint(1, 9)
            else:
                for c in range (0, 9, 1):
                    gameboard[row][c] = 0
                    gameboard[row-1][c] = 0
                col = 0
                row = row - 1
                continue
            col+=1
        col = 0
        row+=1
    create_playing_board()
    # print_board()

def check_equality(row, col):
    # check row
    for c in range(0, 9, 1):
        if gameboard[row][col] == gameboard[row][c]:
            if col != c:
                return True
    # check column
    for r in range(0, 9, 1):
        if gameboard[row][col] == gameboard[r][col]:
            if row != r:
                return True
    # check box
    start_row = row - (row%3)
    start_col = col - (col%3)
    for r in range(start_row, start_row+3, 1):
        for c in range(start_col, start_col+3, 1):
            if gameboard[row][col] == gameboard[r][c]:
                if row != r and col != c:
                    return True
    return False

def check_possible(row, col):
    actual = gameboard[row][col]
    for x in range(1, 10, 1):
        gameboard[row][col] = x
        if not check_equality(row, col):
            gameboard[row][col] = actual
            return True
    gameboard[row][col] = actual
    return False

def create_playing_board():
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            playing_board[row][col] = gameboard[row][col]
    for spot in range (0, blanks, 1):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        while playing_board[x][y] == 0:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
        playing_board[x][y] = 0

def print_board():
    for line in range(0, 9, 1):
        print(gameboard[line])

def draw_board():
    pygame.init()
    global screen
    screen = pygame.display.set_mode([720, 780])
    screen.fill((255, 255, 255))
    # thick lines
    for x in range(1, 3, 1):
        pygame.draw.line(screen, (0, 0, 0), (x*240, 0), (x*240, 720), 8)
        pygame.draw.line(screen, (0, 0, 0), (0, x*240), (720, x*240), 8)
    pygame.draw.line(screen, (0, 0, 0), (0, 720), (720, 720), 8)
    # grid lines                                                        
    for x in range(1, 9, 1):
        pygame.draw.line(screen, (0, 0, 0), (x*80,0), (x*80, 720), 4)
        pygame.draw.line(screen, (0, 0, 0), (0,x*80), (720, x*80), 4)
    # numbers
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if playing_board[row][col] != 0:
                text = val_font.render(str(playing_board[row][col]), True, (0, 0, 0))
                screen.blit(text, ((col*80)+28,(row*80)+15))
    # Attempts and Whether game is over
    text = val_font.render("Score: ", True, (0, 0, 0))
    screen.blit(text, (50, 725))
    for w in range(0, wrongs, 1):
        text = val_font.render("X", True, (255, 0, 0))
        screen.blit(text, (200+(40*w), 725))
    pygame.display.update()
    if blanks == 0:
        ind_win()
    if wrongs > 3:
        ind_loss()

def get_coordinate(pos):
    global curr_x
    curr_x = math.trunc(pos[0]/80)
    global curr_y
    curr_y = math.trunc(pos[1]/80)

def outline_box():
    # draw red box around selected box
    pygame.draw.line(screen, (255, 0, 0), ((curr_x*80), (curr_y*80)), ((curr_x*80)+80, curr_y*80), 8)
    pygame.draw.line(screen, (255, 0, 0), ((curr_x*80)+80, curr_y*80), ((curr_x*80)+80, ((curr_y*80)+80)), 8)
    pygame.draw.line(screen, (255, 0, 0), ((curr_x*80)+80, (curr_y*80)+80), (curr_x*80, (curr_y*80)+80), 8)
    pygame.draw.line(screen, (255, 0, 0), (curr_x*80, (curr_y*80)+80), (curr_x*80, curr_y*80), 8)

def draw_val():
    text = val_font.render(str(val), True, (0, 0, 0))
    screen.blit(text, ((curr_x*80)+26, (curr_y*80)+15))
def ind_wrong():
    text = message_font.render("Wrong value!", True, (255, 0, 0))
    screen.blit(text, (360, 725))
def ind_right():
    text = message_font.render("Correct!", True, (0, 255, 0))
    screen.blit(text, (360, 725))
def ind_win():
    text = message_font.render("You won!", True, (0, 255, 0))
    # global run
    # run = False
    screen.blit(text, (360, 725))
def ind_loss():
    text = message_font.render("You lost... :(", True, (255, 0, 0))
    # global run
    # run = False
    screen.blit(text, (330, 725))

create_board()

run = True
error = 0
reset = 0
on_box = 0
try_box = 0
val_inbox = 0
right_message = 0
wrong_message = 0

while run:
    # print("running")
    # screen.fill((255, 255, 255))
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Get the mouse position to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse clicked")
            pos = pygame.mouse.get_pos()
            right_message = 0
            wrong_message = 0
            val_inbox = 0
            if pos[1] < 720:
                get_coordinate(pos)
                on_box = True
                outline_box()
        if event.type == pygame.KEYDOWN:
            #print("key pressed")
            right_message = 0
            wrong_message = 0
            if event.key == pygame.K_LEFT:
                if curr_x > 0:
                    curr_x -= 1
                    val_inbox = 0
            if event.key == pygame.K_RIGHT:
                if curr_x < 8:
                    curr_x += 1
                    val_inbox = 0
            if event.key == pygame.K_UP:
                if curr_y > 0:
                    curr_y -= 1
                    val_inbox = 0
            if event.key == pygame.K_DOWN:
                if curr_y < 8:
                    curr_y += 1
                    val_inbox = 0 
            if event.key == pygame.K_1:
                val = 1
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_2:
                val = 2
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_3:
                val = 3
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_4:
                val = 4
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_5:
                val = 5
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_6:
                val = 6
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_7:
                val = 7
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_8:
                val = 8
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val()
            if event.key == pygame.K_9:
                val = 9
                # playing_board[curr_y][curr_x] = val
                val_inbox = True
                draw_val() 
            if event.key == pygame.K_RETURN:
                if on_box:
                    if val_inbox:
                        try_box = True
            if event.key == pygame.K_BACKSPACE:
                if val_inbox:
                    val_inbox = False
    if on_box:
        outline_box()
    if val_inbox:
        if playing_board[curr_y][curr_x] == 0:
            draw_val()
    if try_box:
        val_inbox = 0
        if gameboard[curr_y][curr_x] != val:
            ind_wrong()
            wrong_message = 1
            wrongs += 1
            try_box = False
        else:
            try_box = False
            right_message = 1
            ind_right()
            blanks -= 1
            draw_val()
            playing_board[curr_y][curr_x] = val
    if right_message:
        ind_right()
    if wrong_message:
        ind_wrong()
    if wrongs > 2:
        wrong_message = False
        ind_loss()
    if blanks == 0:
        right_message = False
        ind_win()
    pygame.display.update()

pygame.quit()


