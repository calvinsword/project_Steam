import pygame
import math
import time
import random

pygame.font.init()
font = pygame.font.Font(None, 30)
moneyfont = pygame.font.Font(None, 30)
running = True
pygame.init()
White = 255, 255, 255
Black = 0, 0, 0
size = width, height = 1000, 800
screen = pygame.display.set_mode(size, )
screen.fill(White)
mainscreen = False
gamescreen = False
inlogschermU = True
snake_speed = 15
username = ""
# Window size
window_x = 1000
window_y = 800
Running = True

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0


def show_score(choice, color):
    # creating font object score_font
    score_font = moneyfont

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()

    # displaying text
    screen.blit(score_surface, score_rect)
    pygame.draw.rect(screen, White, (800, 0, 200, 30), 3)
    text = font.render("Go Back", False, (255, 255, 255))
    screen.blit(text, (805, 5))


def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # blit will draw the text on screen
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    pygame.draw.rect(screen, White, (800, 0, 200, 30), 3)
    text = font.render("Go Back", False, (255, 255, 255))
    screen.blit(text, (805, 5))

    # deactivating pygame library
    # quit the program


while running:
    time1 = time.time()
    if inlogschermU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(username)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                test = pygame.mouse.get_pressed(num_buttons=3)
                if test[0]:  # true if left click
                    mousepos = pygame.mouse.get_pos()
                    mousey = int(mousepos[0])
                    mousex = int(mousepos[1])

                elif test[1]:  # true if middle click
                    print("yay")
                elif test[2]:  # true if right click
                    print("yay")
                else:  # if scroll wheel is activated
                    print('nah')
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    print("")
                if gamescreen:
                    if event.key == pygame.K_UP:
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'
                    if change_to == 'UP' and direction != 'DOWN':
                        direction = 'UP'
                    if change_to == 'DOWN' and direction != 'UP':
                        direction = 'DOWN'
                    if change_to == 'LEFT' and direction != 'RIGHT':
                        direction = 'LEFT'
                    if change_to == 'RIGHT' and direction != 'LEFT':
                        direction = 'RIGHT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                test = pygame.mouse.get_pressed(num_buttons=3)
                if test[0]:  # true if left click
                    mousepos = pygame.mouse.get_pos()
                    mousey = int(mousepos[0])
                    mousex = int(mousepos[1])
                    if mainscreen:
                        if 1000 > mousey > 800 and 30 > mousex > 0:
                            mainscreen = False
                            gamescreen = True
                    elif gamescreen:
                        if 1000 > mousey > 800 and 30 > mousex > 0:
                            mainscreen = True
                            gamescreen = False

                elif test[1]:  # true if middle click
                    print("yay")
                elif test[2]:  # true if right click
                    print("yay")
                else:  # if scroll wheel is activated
                    print('nah')

    screen.fill(White)
    if mainscreen:
        pygame.draw.rect(screen, Black, (800, 0, 200, 30), 3)
        text = font.render("Im  Bored", False, (0, 0, 0))
        screen.blit(text, (805, 5))

    elif gamescreen:
        if Running:
            screen.fill(black)
            pygame.init()

            # Initialise game window
            pygame.display.set_caption("Gamer Snake")
            game_window = pygame.display.set_mode((window_x, window_y))

            # FPS (frames per second) controller
            fps = pygame.time.Clock()

            # If two keys pressed simultaneously
            # we don't want snake to move into two
            # directions simultaneously
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10

            # Snake body growing mechanism
            # if fruits and snakes collide then scores
            # will be incremented by 10
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 10
                fruit_spawn = False
            else:
                snake_body.pop()

            if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                                  random.randrange(50, (window_y // 10)) * 10]

            fruit_spawn = True

            for pos in snake_body:
                pygame.draw.rect(screen, green,
                                 pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(game_window, white, pygame.Rect(
                fruit_position[0], fruit_position[1], 10, 10))

            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_x - 10:
                game_over()
                Running = False
            if snake_position[1] < 0 or snake_position[1] > window_y - 10:
                game_over()
                Running = False

            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over()

            # displaying score continuously
            show_score(1, white)

            # Refresh game screen
            pygame.display.update()

            # Frame Per Second /Refresh Rate
            fps.tick(snake_speed)
        else:
            screen.fill(black)
            pygame.draw.rect(screen, White, (800, 0, 200, 30), 3)
            text = font.render("Go Back", False, (255, 255, 255))
            screen.blit(text, (805, 5))

    elif inlogschermU:
        text = font.render("Login with your steam Username", False, (0, 0, 0))
        screen.blit(text, (100, 50))
        pygame.draw.rect(screen, Black, (95, 45, 340, 30), 3)
        text = font.render("Username:", False, (0, 0, 0))
        screen.blit(text, (100, 100))
        pygame.draw.rect(screen, Black, (95, 95, 115, 30), 3)
        text = font.render(username, False, (0, 0, 0))
        screen.blit(text, (150, 200))

    pygame.time.wait(0)
    pygame.display.flip()
