import pygame
import math
import time
import random
import json
import requests
import passwords

pygame.font.init()
font = pygame.font.Font(None, 30)
moneyfont = pygame.font.Font(None, 30)
running = True
pygame.init()
registerError = ""
White = 255, 255, 255
Black = 0, 0, 0
size = width, height = 1000, 800
screen = pygame.display.set_mode(size, )
screen.fill(White)
currentSteamID = 0
mainscreen = False
usernameloginerror = ""
gamescreen = False
registerscreen = False
usernamelogin = True
inlogscherm = True
steamidlogin = ""
SteamAPIKey = passwords.SteamAPIKey
snake_speed = 15
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
grey = pygame.Color(137, 148, 153)

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
    if inlogscherm or registerscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if usernamelogin:
                        if event.key == pygame.K_RETURN:
                            print(username)
                            existing_data = []
                            try:
                                with open('valid_steamid.json', 'r') as file:
                                    existing_data = json.load(file)
                            except (FileNotFoundError, json.decoder.JSONDecodeError):
                                pass
                            if inlogscherm:
                                if any(existing.get('name') == username for existing in existing_data if
                                       isinstance(existing, dict)):
                                    for x in existing_data:
                                        if x['name'] == username:
                                            currentSteamID = x['steam_id']
                                    inlogscherm = False
                                    mainscreen = True

                            if len(username) < 4:
                                usernameloginerror = "Please user your username, it has at least 4 characters"
                            elif registerscreen:
                                usernamelogin = False
                            else:
                                usernameloginerror = "This username is not know, please try again or register via the button below"

                        elif event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    if not usernamelogin:
                        if event.key == pygame.K_RETURN:
                            api_url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={SteamAPIKey}&steamids={steamidlogin}'

                            try:
                                response = requests.get(api_url)
                                data = response.json()

                                if 'response' in data and 'players' in data['response']:
                                    players = data['response']['players']

                                    if players:
                                        player_info = {
                                            'steam_id': steamidlogin,
                                            'name': username
                                        }

                                        existing_data = []
                                        try:
                                            with open('valid_steamid.json', 'r') as file:
                                                existing_data = json.load(file)
                                        except (FileNotFoundError, json.decoder.JSONDecodeError):
                                            pass

                                        if not isinstance(existing_data, list):
                                            existing_data = []

                                        with open('valid_steamid.json', 'w') as file:
                                            existing_data.append(player_info)
                                            json.dump(existing_data, file, indent=2)
                                        currentSteamID = steamidlogin
                                        registerscreen = False
                                        mainscreen = True

                                    else:
                                        registerError = "This steamID is not valid"
                                else:
                                    registerError = "The API has given an unexpected response, try again. If the error persists please contact the developers"
                            except requests.RequestException as e:
                                registerError = "Unfortunatly we are not able to connect to the steam API at this moment"

                        elif event.key == pygame.K_BACKSPACE:
                            steamidlogin = steamidlogin[:-1]
                        elif event.unicode in numbers:
                            steamidlogin += str(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                test = pygame.mouse.get_pressed(num_buttons=3)
                if test[0]:  # true if left click
                    mousepos = pygame.mouse.get_pos()
                    mousey = int(mousepos[0])
                    mousex = int(mousepos[1])
                    if inlogscherm:
                        if 650 > mousey > 200 and 540 > mousex > 450:
                            inlogscherm = False
                            registerscreen = True
                    if registerscreen:
                        if 945 > mousey > 605 and 740 > mousex > 650:
                            inlogscherm = True
                            registerscreen = False

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

    screen.fill(grey)
    if mainscreen:
        pygame.draw.rect(screen, Black, (800, 0, 200, 30), 3)
        text = font.render("Im  Bored", False, (0, 0, 0))
        screen.blit(text, (805, 5))
        text = font.render(f"Steam id: {currentSteamID}", False, (0, 0, 0))
        screen.blit(text, (60, 5))
        screen.blit(pygame.image.load("Images/Logo50x50.png", ), (0, 0))

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

    elif inlogscherm:
        text = font.render("Login with your application Username", False, (0, 0, 0))
        screen.blit(text, (100, 50))
        pygame.draw.rect(screen, Black, (95, 45, 400, 30), 3)
        text = font.render(f"Username: {username}", False, (0, 0, 0))
        screen.blit(text, (100, 100))
        pygame.draw.rect(screen, Black, (95, 95, 340, 30), 3)
        text = font.render("If you haven't used this application before press the button below to register", False,
                           (0, 0, 0))
        screen.blit(text, (100, 225))
        text = font.render("Register", False, (0, 0, 0))
        screen.blit(text, (315, 497))
        pygame.draw.rect(screen, Black, (200, 450, 340, 90), 3)
        text = font.render(f"{usernameloginerror}", False, (0, 0, 0))
        screen.blit(text, (100, 175))
        screen.blit(pygame.image.load("Images/Logo125x125.png", ), (850, 10))

    elif registerscreen:
        text = font.render("Create a username:", False, (0, 0, 0))
        screen.blit(text, (100, 50))
        pygame.draw.rect(screen, Black, (95, 45, 340, 30), 3)
        text = font.render(f"Username: {username}", False, (0, 0, 0))
        screen.blit(text, (100, 100))
        pygame.draw.rect(screen, Black, (95, 95, 340, 30), 3)
        text = font.render("Add your steam ID", False, (0, 0, 0))
        screen.blit(text, (100, 150))
        pygame.draw.rect(screen, Black, (95, 145, 340, 30), 3)
        text = font.render(f"Steam ID: {steamidlogin}", False, (0, 0, 0))
        screen.blit(text, (100, 200))
        pygame.draw.rect(screen, Black, (95, 195, 340, 30), 3)
        text = font.render("To find your steam ID:", False, (0, 0, 0))
        screen.blit(text, (100, 400))
        text = font.render("1. open the steam application", False, (0, 0, 0))
        screen.blit(text, (100, 450))
        text = font.render("2. Press on your name in the right top corner", False, (0, 0, 0))
        screen.blit(text, (100, 500))
        text = font.render("3. Go to Account details", False, (0, 0, 0))
        screen.blit(text, (100, 550))
        text = font.render("4. Your steam id is now under your username", False, (0, 0, 0))
        screen.blit(text, (100, 600))
        text = font.render("Go back to login", False, (0, 0, 0))
        screen.blit(text, (615, 690))
        pygame.draw.rect(screen, Black, (605, 650, 340, 90), 3)
        text = font.render(f"{registerError}", False, (0, 0, 0))
        screen.blit(text, (615, 500))
        screen.blit(pygame.image.load("Images/Logo125x125.png", ), (850, 10))

    pygame.time.wait(0)
    pygame.display.flip()
