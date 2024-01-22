import datetime
import webbrowser
import pygame
import json
import requests
import passwords
import API
import game_url
from serial.tools import list_ports
import serial


pygame.font.init()
font = pygame.font.Font(None, 30)
smallFont = pygame.font.Font(None, 25)
bigFont = pygame.font.Font(None, 40)
running = True
pygame.init()
Friends = ""
registerError = ""
White = 255, 255, 255
Black = 0, 0, 0
size = width, height = 1000, 800
screen = pygame.display.set_mode(size, )
screen.fill(White)
currentSteamID = 0
FriendsScrolling = 0
time2 = 0
time1 = 0
mainscreen = False
timerscreen = False
registerscreen = False
inlogscherm = True
usernameloginerror = ""
steamidlogin = ""
SteamAPIKey = passwords.SteamAPIKey
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
username = ""
# Window size
window_x = 1000
window_y = 800
usernamelogin = True
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
grey = pygame.Color(137, 148, 153)
timerM = 0


def openWebsite(nameOfTheGame):
    gameurl = game_url.get_steam_game_info_by_name(nameOfTheGame)
    webbrowser.open(gameurl)


while running:
    if inlogscherm or registerscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if usernamelogin:
                        if event.key == pygame.K_RETURN:
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
                                usernameloginerror = "This username is not know, please try again or register via " \
                                                     "the button below"

                        elif event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    if not usernamelogin:
                        if event.key == pygame.K_RETURN:
                            api_url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?' \
                                      f'key={SteamAPIKey}&steamids={steamidlogin}'

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
                                    registerError = "The API has given an unexpected response, try again. If the " \
                                                    "error persists please contact the developers"
                            except requests.RequestException as e:
                                registerError = "Unfortunatly we are not able to connect to the steam API at this " \
                                                "moment"

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
                    continue
                elif test[2]:  # true if right click
                    continue
                else:  # if scroll wheel is activated
                    continue
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                test = pygame.mouse.get_pressed(num_buttons=3)
                if test[0]:  # true if left click
                    mousepos = pygame.mouse.get_pos()
                    mousey = int(mousepos[0])
                    mousex = int(mousepos[1])
                    if mainscreen:
                        if 400 > mousey > 0 and 705 > mousex > 655:
                            openWebsite(Friends[FriendsScrolling % len(Friends)][1])
                        elif 400 > mousey > 0 and 755 > mousex > 705:
                            openWebsite(Friends[(FriendsScrolling + 1) % len(Friends)][1])
                        elif 400 > mousey > 0 and 805 > mousex > 755:
                            openWebsite(Friends[(FriendsScrolling + 2) % len(Friends)][1])
                        elif 1000 > mousey > 935 and 30 > mousex > 0:
                            timerscreen = True
                            mainscreen = False
                    elif timerscreen:
                        if 250 > mousex > 200:
                            if mousey < 200:
                                timerM += 1
                            elif mousey > 800:
                                timerM += 30
                            elif 600 > mousey > 400:
                                timerM += 5
                        elif 320 > mousex > 270:
                            if mousey < 200 and timerM >= 1:
                                timerM -= 1
                            if mousey > 800 and timerM >= 30:
                                timerM -= 30
                            if 600 > mousey > 400 and timerM >= 5:
                                timerM -= 5
                        elif 455 > mousex > 380:
                            if 600 > mousey > 400:
                                registerError = ""
                                if timerM <= 0:
                                    registerError = "The time must be more then 0 minutes"
                                else:
                                    registerError = "The timer has started"


                                    def read_serial(port):
                                        line = port.read(1000)
                                        return line.decode()


                                    serial_ports = list_ports.comports()

                                    pico_port = serial_ports[0].device

                                    # Open a connection to the Pico
                                    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N',
                                                       stopbits=1, timeout=1) as serial_port:
                                        time_in_seconds = (timerM * 60)

                                        time_in_seconds_pico_acceptable = str(time_in_seconds) + "\r"
                                        serial_port.write(time_in_seconds_pico_acceptable.encode())
                                        pico_output = read_serial(serial_port)
                                    serial_port.close()

                            elif 200 > mousey:
                                timerM = 0

                        elif 1000 > mousey > 935 and 30 > mousex > 0:
                            mainscreen = True
                            timerscreen = False

                        elif 600 > mousey > 400 and 455 > mousex > 380:
                            timerM = 0

                elif test[1]:  # true if middle click
                    continue
                elif test[2]:  # true if right click
                    continue
                else:  # if scroll wheel is activated
                    FriendsScrolling += 1

    screen.fill(grey)

    if mainscreen:
        text = font.render(f"Steam id: {currentSteamID}", False, (0, 0, 0))
        screen.blit(text, (60, 5))
        screen.blit(pygame.image.load("Images/Logo50x50.png", ), (0, 0))
        text = font.render("Timer", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, Black, (935, 0, 65, 30), 3)
        text = bigFont.render("The best games on steam", False, (0, 0, 0))
        screen.blit(text, (500, 750))
        pygame.draw.rect(screen, Black, (450, 725, 450, 75), 3)
        time2 = datetime.datetime.now().timestamp() - time1
        if time2 > 5:
            time1 = datetime.datetime.now().timestamp()
            Friends2 = API.printOnlineFriends(SteamAPIKey, currentSteamID)
            if Friends2 != Friends:
                Friends = Friends2
        Friends = [["testuser1", "Rounds"], ["testuser2", "Bitburner"],
                   ["testuser3", "Paladins"], ["testuser4", "Runescape"]]
        if not Friends:
            text = font.render("None of your friends are currently using steam", False, (0, 0, 0))
            screen.blit(text, (0, 630))
        else:
            text = font.render("Your friends are playing:", False, (0, 0, 0))
            screen.blit(text, (0, 630))
            text = smallFont.render(f"{Friends[FriendsScrolling % len(Friends)][0]}: ", False, (0, 0, 0))
            screen.blit(text, (5, 660))
            text = smallFont.render(f"{Friends[FriendsScrolling % len(Friends)][1]} ", False, (0, 0, 0))
            screen.blit(text, (5, 680))
            pygame.draw.rect(screen, Black, (0, 655, 400, 50), 3)
            if len(Friends) > 1:
                text = smallFont.render(f"{Friends[(FriendsScrolling + 1) % len(Friends)][0]}: ", False, (0, 0, 0))
                screen.blit(text, (5, 710))
                text = smallFont.render(f"{Friends[(FriendsScrolling + 1) % len(Friends)][1]} ", False, (0, 0, 0))
                screen.blit(text, (5, 730))
                pygame.draw.rect(screen, Black, (0, 705, 400, 50), 3)
            if len(Friends) > 2:
                text = smallFont.render(f"{Friends[(FriendsScrolling + 2) % len(Friends)][0]}: ", False, (0, 0, 0))
                screen.blit(text, (5, 760))
                text = smallFont.render(f"{Friends[(FriendsScrolling + 2) % len(Friends)][1]} ", False, (0, 0, 0))
                screen.blit(text, (5, 780))
                pygame.draw.rect(screen, Black, (0, 755, 400, 50), 3)

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

    elif timerscreen:
        screen.blit(pygame.image.load("Images/Logo50x50.png", ), (0, 0))
        text = font.render("Back", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, Black, (935, 0, 65, 30), 3)
        text = bigFont.render(f"The timer is set to {timerM} minutes", False, (0, 0, 0))
        screen.blit(text, (350, 100))

        text = font.render("+1 Min", False, (0, 0, 0))
        screen.blit(text, (68, 215))
        pygame.draw.rect(screen, Black, (0, 200, 200, 50), 3)

        text = font.render("-1 Min", False, (0, 0, 0))
        screen.blit(text, (72, 285))
        pygame.draw.rect(screen, Black, (0, 270, 200, 50), 3)

        text = font.render("+5 Min", False, (0, 0, 0))
        screen.blit(text, (468, 215))
        pygame.draw.rect(screen, Black, (400, 200, 200, 50), 3)

        text = font.render("-5 Min", False, (0, 0, 0))
        screen.blit(text, (472, 285))
        pygame.draw.rect(screen, Black, (400, 270, 200, 50), 3)

        text = font.render("+30 Min", False, (0, 0, 0))
        screen.blit(text, (866, 215))
        pygame.draw.rect(screen, Black, (800, 200, 200, 50), 3)

        text = font.render("-30 Min", False, (0, 0, 0))
        screen.blit(text, (870, 285))
        pygame.draw.rect(screen, Black, (800, 270, 200, 50), 3)

        text = bigFont.render("Start Timer", False, (0, 0, 0))
        screen.blit(text, (428, 400))
        pygame.draw.rect(screen, Black, (400, 380, 200, 75), 3)

        text = bigFont.render("Reset Timer", False, (0, 0, 0))
        screen.blit(text, (23, 400))
        pygame.draw.rect(screen, Black, (000, 380, 200, 75), 3)

        text = bigFont.render(f"{registerError}", False, (0, 0, 0))
        screen.blit(text, (23, 600))

    pygame.time.wait(0)
    pygame.display.flip()

# TODO Separate page for top games /statistics (27 genres)
# TODO Timer met hardware
