import datetime
from datetime import datetime, timedelta
import webbrowser
import pygame
import json
import requests
import passwords
import API
import game_url
from serial.tools import list_ports
import serial
import Statistics
import matplotlib.pyplot as plt

# de setup voor de verschillende text-fonts in de GUI
pygame.font.init()
font = pygame.font.Font(None, 30)
smallFont = pygame.font.Font(None, 25)
bigFont = pygame.font.Font(None, 40)

# het definiëren van kleuren voor PyGame
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
grey = pygame.Color(137, 148, 153)

# de start voor de loop van pygame
running = True
pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size, )
screen.fill(white)

# setup van een aantal variabelen om errors te voorkomen met non declared variables
Friends = ""
registerError = ""
usernameloginerror = ""
bestgamesArray = ""
bestgamegenre = ""
username = ""
steamidlogin = ""
currentSteamID = 0
FriendsScrolling = 0
time2 = 0
time1 = 0
timerM = 0
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
Buzzer = "On"

# neerzetten van de booleans voor de verschillende schermen
mainscreen = False
timerscreen = False
bestGame = False
registerscreen = False
inlogscherm = True
playtimePrice = False
playtime = False
displaytop5games = False
usernamelogin = True
STEAM_API_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'


def quicksort_games_by_playtime(games):
    if len(games) <= 1:
        return games

    pivot = games[len(games) // 2]['playtime_2weeks']
    left = [game for game in games if game['playtime_2weeks'] > pivot]
    middle = [game for game in games if game['playtime_2weeks'] == pivot]
    right = [game for game in games if game['playtime_2weeks'] < pivot]

    return quicksort_games_by_playtime(left) + middle + quicksort_games_by_playtime(right)


# definieer een functie voor het openen van een website met de naam van een steam game
def openWebsite(nameOfTheGame):
    gameurl = game_url.get_steam_game_info_by_name(nameOfTheGame)
    webbrowser.open(gameurl)


def get_recent_playtime(steam_id):
    two_weeks_ago = int((datetime.now() - timedelta(days=14)).timestamp())

    params = {
        'key': passwords.SteamAPIKey,
        'steamid': steam_id,
        'format': 'json',
        'include_played_free_games': 1,
        'include_appinfo': 1,
        'include_free_sub': 1,
    }

    response = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params=params)

    if response.status_code == 200:
        data = response.json()
        games = data['response']['games']

        # Filter out games with playtime equal to 0 or last played before two weeks ago
        games = [game for game in games if game['playtime_forever'] > 0 and game.get('playtime_2weeks', 0) > 0]

        return quicksort_games_by_playtime(games)
    else:
        print(f"Failed to fetch playtime data. Status code: {response.status_code}")
        return None


def plot_playtime_graph(steam_id):
    games = get_recent_playtime(steam_id)
    game_names = [game['name'] for game in games]
    playtimes = [game['playtime_2weeks'] // 60 for game in
                 games]  # Corrected playtime calculation to use playtime_2weeks

    total_playtime = sum(playtimes)

    game_names.append('Total Playtime')
    playtimes.append(total_playtime)

    plt.bar(['Total Playtime'], [total_playtime], color='green')  # Total playtime on the left

    # Bar chart for individual games
    plt.bar(game_names, playtimes, color='blue')

    plt.xlabel('Games')
    plt.ylabel('Playtime (hours)')
    plt.title('Steam Game Playtime in the Last 2 Weeks')
    plt.xticks(rotation=45, ha='right')
    plt.savefig("Images/Playtime.png")


while running:  # start the main loop
    if inlogscherm or registerscreen:  # if you are in the login/register screen there are different effects on events
        for event in pygame.event.get():  # listen to events
            if event.type == pygame.QUIT:  # if you click the red cross close the program
                quit()
            if event.type == pygame.KEYDOWN:  # if the event is that the user pressed a key
                if usernamelogin:  # if it is the the username string not the steam id
                    if event.key == pygame.K_RETURN:  # if it is the enter button
                        existing_data = []  # make an empty array/ empty it
                        try:
                            with open('valid_steamid.json', 'r') as file:
                                existing_data = json.load(file)  # if the file doesnt exist give an error
                        except (FileNotFoundError, json.decoder.JSONDecodeError):
                            pass
                        if inlogscherm:  # if you are in the login file
                            if any(existing.get('name') == username for existing in existing_data if
                                   # check if the username is known
                                   isinstance(existing, dict)):
                                for x in existing_data:  # get the steam id connected to the username
                                    if x['name'] == username:
                                        currentSteamID = x['steam_id']
                                plot_playtime_graph(
                                    currentSteamID)  # get the plot of the users playtime in the past 2 weeks
                                inlogscherm = False  # stop the login process f it is succesfull
                            mainscreen = True  # turn on the main program page

                            if len(username) < 4:  # give an error if the username is shorter then 4 characters
                                usernameloginerror = "Please user your username, it has at least 4 characters"
                            elif registerscreen:  # change the typing square to the steam id if you registering
                                usernamelogin = False
                            else:  # throw a different error if the name isnt known
                                usernameloginerror = "This username is not know, please try again or register via " \
                                                     "the button below"
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]  # drop the last character of the string on a backspace
                    else:
                        username += event.unicode  # add the character to the string
                    if not usernamelogin:  # if you are registering
                        if event.key == pygame.K_RETURN:  # on enter check if the steam ID is correct
                            api_url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?' \
                                      f'key={passwords.SteamAPIKey}&steamids={steamidlogin}'
                            # Create a link to call the API of steam
                            try:
                                response = requests.get(api_url)
                                data = response.json()
                                # get the Data
                                if 'response' in data and 'players' in data['response']:  #
                                    players = data['response']['players']
                                    # check if the information the user filled in is correct
                                    if players:
                                        player_info = {
                                            'steam_id': steamidlogin,
                                            'name': username
                                        }
                                        # link the json values to the variables
                                        existing_data = []
                                        try:
                                            with open('valid_steamid.json', 'r') as file:
                                                existing_data = json.load(file)
                                        except (FileNotFoundError, json.decoder.JSONDecodeError):
                                            pass
                                        # open the json file and load the variables
                                        if not isinstance(existing_data, list):
                                            existing_data = []  # make the steam id used to log in the running steam id
                                        # add the data if it doesn't exist yet
                                        with open('valid_steamid.json', 'w') as file:
                                            existing_data.append(player_info)
                                            json.dump(existing_data, file, indent=2)
                                        currentSteamID = steamidlogin
                                        plot_playtime_graph(currentSteamID)
                                        registerscreen = False  # turn off the register screen
                                        mainscreen = True  # turn on the main application screen

                                    else:
                                        registerError = "This steamID is not valid"
                                        # show an error if the username is not known
                                else:
                                    registerError = "The API has given an unexpected response, try again. If the " \
                                                    "error persists please contact the developers"
                                    # give an error if the API call returns something unexpected
                            except requests.RequestException as e:
                                registerError = "Unfortunatly we are not able to connect to the steam API at this " \
                                                "moment"
                                # throw an error if the steam API is down

                        elif event.key == pygame.K_BACKSPACE:
                            steamidlogin = steamidlogin[:-1]  # drop the last character of the steam i on backspace
                        elif event.unicode in numbers:  # if the character the user put in add it to the steam id
                            steamidlogin += str(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:  # if the event is a mouseclick
                test = pygame.mouse.get_pressed(num_buttons=3)  # convert the mousebuttons to a tuple
                if test[0]:  # true if left click
                    mousepos = pygame.mouse.get_pos()  # change the mouse position from the event to an array
                    mousey = int(mousepos[0])  # change the mouse array to 2 seperate ints
                    mousex = int(mousepos[1])
                    if inlogscherm:  # change the screen if the left click is between the 2 values
                        if 650 > mousey > 200 and 540 > mousex > 450:
                            inlogscherm = False
                            registerscreen = True
                    if registerscreen:  # change the screen if the left click is between the 2 values
                        if 945 > mousey > 605 and 740 > mousex > 650:
                            inlogscherm = True
                            registerscreen = False

                elif test[1]:  # true if middle click no functionality
                    continue
                elif test[2]:  # true if right click no functionality
                    continue
                else:  # if scroll wheel is activated no functionality
                    continue
    else:  # if the user isn't logging in
        for event in pygame.event.get():  # gether user events
            if event.type == pygame.QUIT:  # if pressed on the red cross close the program
                quit()
            elif event.type == pygame.KEYDOWN:
                continue  # no functionality
            elif event.type == pygame.MOUSEBUTTONDOWN:  # same code as for the login screens
                test = pygame.mouse.get_pressed(num_buttons=3)
                if test[0]:  # true if left click
                    mousepos = pygame.mouse.get_pos()
                    mousey = int(mousepos[0])
                    mousex = int(mousepos[1])
                    if mainscreen:
                        if 400 > mousey > 0 and 705 > mousex > 655:  # this is a repeating line of code to check if the
                            # user pressed on one of the buttons
                            openWebsite(Friends[FriendsScrolling % len(Friends)][1])  # open the steam page of the game the frind is playing
                        elif 400 > mousey > 0 and 755 > mousex > 705:
                            openWebsite(Friends[(FriendsScrolling + 1) % len(Friends)][1])
                        elif 400 > mousey > 0 and 805 > mousex > 755:
                            openWebsite(Friends[(FriendsScrolling + 2) % len(Friends)][1])
                        elif 400 > mousey > 275 and 655 > mousex > 625:
                            FriendsScrolling = 0  # reset the scrolling in the friends list
                        elif 1000 > mousey > 935 and 30 > mousex > 0:
                            timerscreen = True  # switch to the timer
                            mainscreen = False
                        elif 900 > mousey > 450 and 800 > mousex > 725:
                            bestGame = True  # switch to the top steam games
                            mainscreen = False
                        elif 300 > mousey > 0 and 230 > mousex > 190:
                            playtimePrice = True  # switch to the playtime/price distribution
                            mainscreen = False
                        elif 300 > mousey > 0 and 190 > mousex > 150:
                            playtime = True  # switch to the screen seeing your playtime in the last 2 weeks
                            mainscreen = False
                            plot_playtime_graph(currentSteamID)  # plot the playtime
                    elif playtime:
                        if 1000 > mousey > 935 and 30 > mousex > 0:
                            mainscreen = True   # Go back to the mainscreen
                            playtime = False
                    elif timerscreen:
                        if 250 > mousex > 200:
                            if mousey < 200:
                                timerM += 1  # increment the timer by 1 minute
                            elif mousey > 800:
                                timerM += 30  # increment the timer by 30 minute
                            elif 600 > mousey > 400:
                                timerM += 5  # increment the timer by 5 minute
                        elif 320 > mousex > 270:
                            if mousey < 200 and timerM >= 1:
                                timerM -= 1  # decrease the timer by 1 minute
                            if mousey > 800 and timerM >= 30:
                                timerM -= 30  # decrease the timer by 30 minute
                            if 600 > mousey > 400 and timerM >= 5:
                                timerM -= 5  # decrease the timer by 5 minute
                        elif 455 > mousex > 380:
                            if 600 > mousey > 400:
                                registerError = ""  # reset the error message
                                if timerM <= 0:  # throw an error if the timer isnt bigger then 1 minute
                                    registerError = "The time must be more then 0 minutes"
                                else:  # start the timer
                                    registerError = "The timer has started"
                                    timerM = 0  # reset the timer on starting it


                                    def read_serial(port):
                                        line = port.read(1000)
                                        return line.decode()


                                    serial_ports = list_ports.comports()

                                    pico_port = serial_ports[0].device

                                    # Open a connection to the Pico
                                    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N',
                                                       stopbits=1, timeout=1) as serial_port:
                                        timer_time = timerM * 60  # start the timer in seconds
                                        if Buzzer == "On": # tranfer the busser name to  a number
                                            buzzer = 1
                                        else:
                                            buzzer = 0
                                        # Write on the pico LCD the time
                                        serial_input = str(buzzer) + "," + str(timer_time) + "\r"
                                        serial_port.write(serial_input.encode())
                                        serial_port.close()
                            elif 200 > mousey:
                                timerM = 0  # reset the timer
                            elif 1000 > mousey > 800:
                                if Buzzer == "On":  # flip the buzzer from on and off and reverse
                                    Buzzer = "Off"
                                elif Buzzer == "Off":
                                    Buzzer = "On"

                        elif 1000 > mousey > 935 and 30 > mousex > 0:
                            mainscreen = True  # go back to the main screen
                            timerscreen = False
                    elif bestGame:
                        bestgamegenre = ""  # reset the genre the user is searching
                        if 1000 > mousey > 935 and 30 > mousex > 0:
                            mainscreen = True  # go back to the mainscreen
                            bestGame = False
                        if mousey < 200:  # pick the genre for the top 5 games
                            if 100 > mousex > 50:
                                bestgamegenre = "Action"
                            if 200 > mousex > 150:
                                bestgamegenre = "Adventure"
                            if 300 > mousex > 250:
                                bestgamegenre = "Animation & modeling"
                            if 400 > mousex > 350:
                                bestgamegenre = "Casual"
                            if 500 > mousex > 450:
                                bestgamegenre = "Design & illustration"
                            if 600 > mousex > 550:
                                bestgamegenre = "Education"
                        if 600 > mousey > 400:
                            if 100 > mousex > 50:
                                bestgamegenre = "Indie"
                            if 200 > mousex > 150:
                                bestgamegenre = "Massively Multiplayer"
                            if 300 > mousex > 250:
                                bestgamegenre = "RPG"
                            if 400 > mousex > 350:
                                bestgamegenre = "Racing"
                            if 500 > mousex > 450:
                                bestgamegenre = "Simulation"
                            if 600 > mousex > 550:
                                bestgamegenre = "Software training"
                        if 1000 > mousey > 800:
                            if 100 > mousex > 50:
                                bestgamegenre = "Sports"
                            if 200 > mousex > 150:
                                bestgamegenre = "Strategy"
                            if 300 > mousex > 250:
                                bestgamegenre = "Utilities"
                            if 400 > mousex > 350:
                                bestgamegenre = "Video production"
                            if 500 > mousex > 450:
                                bestgamegenre = "Violent"
                            if 600 > mousex > 550:
                                bestgamegenre = "Web publishing"
                        if bestgamegenre != "":  # search the top 5 games of the selected genre and go to that screen
                            bestgamesArray = Statistics.top_games_in_genre(Statistics.read_json_file("steam.json"),
                                                                           bestgamegenre)
                            bestGame = False
                            displaytop5games = True
                    elif displaytop5games:
                        if 1000 > mousey > 935 and 30 > mousex > 0:
                            displaytop5games = False  # return to the genre selector
                            bestGame = True
                    elif playtimePrice:
                        if 1000 > mousey > 935 and 30 > mousex > 0:
                            mainscreen = True
                            playtimePrice = True
                elif test[1]:  # true if middle click
                    continue
                elif test[2]:  # true if right click
                    continue
                else:  # if scroll wheel is activated
                    FriendsScrolling += 1  # scroll trough the friendslist

    screen.fill(grey)  # colour the screen grey

    if mainscreen:  # run this cde if the main apllication screen
        text = font.render(f"Steam id: {currentSteamID}", False, (0, 0, 0))
        screen.blit(text, (60, 5))  # this is the text render function, recurring
        screen.blit(pygame.image.load("Images/Logo50x50.png", ), (0, 0))  # load the logo
        text = font.render("Timer", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, black, (935, 0, 65, 30), 3)  # button to open timer
        text = bigFont.render("The best games on steam", False, (0, 0, 0))
        screen.blit(text, (500, 750))
        pygame.draw.rect(screen, black, (450, 725, 450, 75), 3)  # button to open the best games
        text = font.render("Price/playtime distribution", False, (0, 0, 0))
        screen.blit(text, (5, 200))
        pygame.draw.rect(screen, black, (0, 190, 300, 40), 3)  # open the price/playtime comparer
        text = font.render("Playtime in the past 2 weeks", False, (0, 0, 0))
        screen.blit(text, (5, 160))
        pygame.draw.rect(screen, black, (0, 150, 300, 40), 3)  # open the playtime graph
        time2 = datetime.now().timestamp() - time1  # keep track of the time since the last update
        if time2 > 5:  # if it has been over 5 seconds reload the friends list
            time1 = datetime.now().timestamp()
            Friends2 = API.printOnlineFriends(passwords.SteamAPIKey, currentSteamID)  # run the api to get the friends list
            if type(Friends2) == bool:  # if the function returns a bool the API is turned off
                Friends = ["Error"]
                continue
            elif Friends2 != Friends:
                Friends = Friends2  # update the stored friends list

        # Friends = [["testuser1", "Rounds"], ["testuser2", "Bitburner"],
        # ["testuser3", "Paladins"], ["testuser4", "Runescape"]]
        # Backup friendslist for testing
        if len(Friends) > 0:  # throw an error if the api is set to private
            if Friends[0] == "Error":
                text = font.render("Your friends list is set to private in steam", False, (0, 0, 0))
                screen.blit(text, (0, 660))

        if type(Friends) == list and len(Friends) == 0:  # show this message if there is no one of the users friends online
            text = font.render("None of your friends are currently using steam", False, (0, 0, 0))
            screen.blit(text, (0, 630))

        if len(Friends) > 0 and Friends[0] != "Error":  # show the friends
            text = font.render("Your friends are playing:", False, (0, 0, 0))
            screen.blit(text, (0, 630))
            text = font.render("Back to Top", False, (0, 0, 0))
            screen.blit(text, (280, 630))
            pygame.draw.rect(screen, black, (275, 625, 125, 30), 3)
            text = smallFont.render(f"{Friends[FriendsScrolling % len(Friends)][0]}: ", False, (0, 0, 0))
            # Friends[FriendsScrolling % len(Friends)][0] this code takes the scrolling factor into consideration
            # to show to the user
            screen.blit(text, (5, 660))
            text = smallFont.render(f"{Friends[FriendsScrolling % len(Friends)][1]} ", False, (0, 0, 0))
            screen.blit(text, (5, 680))
            pygame.draw.rect(screen, black, (0, 655, 400, 50), 3)
            if len(Friends) > 1:
                text = smallFont.render(f"{Friends[(FriendsScrolling + 1) % len(Friends)][0]}: ", False, (0, 0, 0))
                screen.blit(text, (5, 710))
                text = smallFont.render(f"{Friends[(FriendsScrolling + 1) % len(Friends)][1]} ", False, (0, 0, 0))
                screen.blit(text, (5, 730))
                pygame.draw.rect(screen, black, (0, 705, 400, 50), 3)
            if len(Friends) > 2:
                text = smallFont.render(f"{Friends[(FriendsScrolling + 2) % len(Friends)][0]}: ", False, (0, 0, 0))
                screen.blit(text, (5, 760))
                text = smallFont.render(f"{Friends[(FriendsScrolling + 2) % len(Friends)][1]} ", False, (0, 0, 0))
                screen.blit(text, (5, 780))
                pygame.draw.rect(screen, black, (0, 755, 400, 50), 3)

    elif inlogscherm:  # display the information for loggin in
        text = font.render("Login with your application Username", False, (0, 0, 0))
        screen.blit(text, (100, 50))
        pygame.draw.rect(screen, black, (95, 45, 400, 30), 3)
        text = font.render(f"Username: {username}", False, (0, 0, 0))
        screen.blit(text, (100, 100))
        pygame.draw.rect(screen, black, (95, 95, 340, 30), 3)
        text = font.render("If you haven't used this application before press the button below to register", False,
                           (0, 0, 0))
        screen.blit(text, (100, 225))
        text = font.render("Register", False, (0, 0, 0))
        screen.blit(text, (315, 497))
        pygame.draw.rect(screen, black, (200, 450, 340, 90), 3)
        text = font.render(f"{usernameloginerror}", False, (0, 0, 0))
        screen.blit(text, (100, 175))
        screen.blit(pygame.image.load("Images/Logo125x125.png", ), (850, 10))

    elif registerscreen:  # display the information to regitser an account
        text = font.render("Create a username:", False, (0, 0, 0))
        screen.blit(text, (100, 50))
        pygame.draw.rect(screen, black, (95, 45, 340, 30), 3)
        text = font.render(f"Username: {username}", False, (0, 0, 0))
        screen.blit(text, (100, 100))
        pygame.draw.rect(screen, black, (95, 95, 340, 30), 3)
        text = font.render("Add your steam ID", False, (0, 0, 0))
        screen.blit(text, (100, 150))
        pygame.draw.rect(screen, black, (95, 145, 340, 30), 3)
        text = font.render(f"Steam ID: {steamidlogin}", False, (0, 0, 0))
        screen.blit(text, (100, 200))
        pygame.draw.rect(screen, black, (95, 195, 340, 30), 3)
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
        pygame.draw.rect(screen, black, (605, 650, 340, 90), 3)
        text = font.render(f"{registerError}", False, (0, 0, 0))
        screen.blit(text, (615, 500))
        screen.blit(pygame.image.load("Images/Logo125x125.png", ), (850, 10))

    elif timerscreen:  # display the timer information
        screen.blit(pygame.image.load("Images/Logo50x50.png", ), (0, 0))
        text = font.render("Back", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, black, (935, 0, 65, 30), 3)
        text = bigFont.render(f"The timer is set to {timerM} minutes", False, (0, 0, 0))
        screen.blit(text, (350, 100))

        text = font.render("+1 Min", False, (0, 0, 0))
        screen.blit(text, (68, 215))
        pygame.draw.rect(screen, black, (0, 200, 200, 50), 3)

        text = font.render("-1 Min", False, (0, 0, 0))
        screen.blit(text, (72, 285))
        pygame.draw.rect(screen, black, (0, 270, 200, 50), 3)

        text = font.render("+5 Min", False, (0, 0, 0))
        screen.blit(text, (468, 215))
        pygame.draw.rect(screen, black, (400, 200, 200, 50), 3)

        text = font.render("-5 Min", False, (0, 0, 0))
        screen.blit(text, (472, 285))
        pygame.draw.rect(screen, black, (400, 270, 200, 50), 3)

        text = font.render("+30 Min", False, (0, 0, 0))
        screen.blit(text, (866, 215))
        pygame.draw.rect(screen, black, (800, 200, 200, 50), 3)

        text = font.render("-30 Min", False, (0, 0, 0))
        screen.blit(text, (870, 285))
        pygame.draw.rect(screen, black, (800, 270, 200, 50), 3)

        text = bigFont.render("Start Timer", False, (0, 0, 0))
        screen.blit(text, (428, 400))
        pygame.draw.rect(screen, black, (400, 380, 200, 75), 3)

        text = bigFont.render("Reset Timer", False, (0, 0, 0))
        screen.blit(text, (23, 400))
        pygame.draw.rect(screen, black, (000, 380, 200, 75), 3)

        text = bigFont.render(f"Buzzer: {Buzzer}", False, (0, 0, 0))
        screen.blit(text, (828, 400))
        pygame.draw.rect(screen, black, (800, 380, 200, 75), 3)

        text = bigFont.render(f"{registerError}", False, (0, 0, 0))
        screen.blit(text, (23, 600))  # dynamically display the error

    elif bestGame:  # display the different genres
        text = font.render("Back", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, black, (935, 0, 65, 30), 3)

        text = bigFont.render("Choose a genre", False, (0, 0, 0))
        screen.blit(text, (0, 0))

        text = bigFont.render("Action", False, (0, 0, 0))
        screen.blit(text, (5, 55))
        pygame.draw.rect(screen, black, (0, 50, 200, 50), 3)

        text = bigFont.render("Adventure", False, (0, 0, 0))
        screen.blit(text, (5, 155))
        pygame.draw.rect(screen, black, (0, 150, 200, 50), 3)

        text = bigFont.render("Animation", False, (0, 0, 0))
        screen.blit(text, (5, 255))
        pygame.draw.rect(screen, black, (0, 250, 200, 50), 3)

        text = bigFont.render("Casual", False, (0, 0, 0))
        screen.blit(text, (5, 355))
        pygame.draw.rect(screen, black, (0, 350, 200, 50), 3)

        text = bigFont.render("Design", False, (0, 0, 0))
        screen.blit(text, (5, 455))
        pygame.draw.rect(screen, black, (0, 450, 200, 50), 3)

        text = bigFont.render("Education", False, (0, 0, 0))
        screen.blit(text, (5, 555))
        pygame.draw.rect(screen, black, (0, 550, 200, 50), 3)

        text = bigFont.render("Indie", False, (0, 0, 0))
        screen.blit(text, (405, 55))
        pygame.draw.rect(screen, black, (400, 50, 200, 50), 3)

        text = bigFont.render("MMO", False, (0, 0, 0))
        screen.blit(text, (405, 155))
        pygame.draw.rect(screen, black, (400, 150, 200, 50), 3)

        text = bigFont.render("RPG", False, (0, 0, 0))
        screen.blit(text, (405, 255))
        pygame.draw.rect(screen, black, (400, 250, 200, 50), 3)

        text = bigFont.render("Racing", False, (0, 0, 0))
        screen.blit(text, (405, 355))
        pygame.draw.rect(screen, black, (400, 350, 200, 50), 3)

        text = bigFont.render("Simulation", False, (0, 0, 0))
        screen.blit(text, (405, 455))
        pygame.draw.rect(screen, black, (400, 450, 200, 50), 3)

        text = bigFont.render("Software", False, (0, 0, 0))
        screen.blit(text, (405, 555))
        pygame.draw.rect(screen, black, (400, 550, 200, 50), 3)

        text = bigFont.render("Sports", False, (0, 0, 0))
        screen.blit(text, (805, 55))
        pygame.draw.rect(screen, black, (800, 50, 200, 50), 3)

        text = bigFont.render("Strategy", False, (0, 0, 0))
        screen.blit(text, (805, 155))
        pygame.draw.rect(screen, black, (800, 150, 200, 50), 3)

        text = bigFont.render("Utilities", False, (0, 0, 0))
        screen.blit(text, (805, 255))
        pygame.draw.rect(screen, black, (800, 250, 200, 50), 3)

        text = bigFont.render("Video Prod", False, (0, 0, 0))
        screen.blit(text, (805, 355))
        pygame.draw.rect(screen, black, (800, 350, 200, 50), 3)

        text = bigFont.render("Violent", False, (0, 0, 0))
        screen.blit(text, (805, 455))
        pygame.draw.rect(screen, black, (800, 450, 200, 50), 3)

        text = bigFont.render("Web", False, (0, 0, 0))
        screen.blit(text, (805, 555))
        pygame.draw.rect(screen, black, (800, 550, 200, 50), 3)

    elif displaytop5games:  # display the 5 best games for the selected genre
        text = font.render("Back", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, black, (935, 0, 65, 30), 3)

        text = bigFont.render(f"These are the top 5 games of the genre: {bestgamegenre}", False, (0, 0, 0))
        screen.blit(text, (5, 55))

        text = bigFont.render(bestgamesArray[0], False, (0, 0, 0))
        screen.blit(text, (5, 155))

        text = bigFont.render(bestgamesArray[1], False, (0, 0, 0))
        screen.blit(text, (5, 255))

        text = bigFont.render(bestgamesArray[2], False, (0, 0, 0))
        screen.blit(text, (5, 355))

        text = bigFont.render(bestgamesArray[3], False, (0, 0, 0))
        screen.blit(text, (5, 455))

        text = bigFont.render(bestgamesArray[4], False, (0, 0, 0))
        screen.blit(text, (5, 555))

    elif playtime:  # display the image for the playtime
        text = font.render("Back", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, black, (935, 0, 65, 30), 3)
        screen.blit(pygame.image.load("Images/Playtime.png", ), (50, 50))

    elif playtimePrice:  # display the image for the GamePrice
        text = font.render("Back", False, (0, 0, 0))
        screen.blit(text, (940, 5))
        pygame.draw.rect(screen, black, (935, 0, 65, 30), 3)
        screen.blit(pygame.image.load("Images/GamePrice.png", ), (50, 50))

    pygame.time.wait(0)
    pygame.display.flip()
