import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Replace '7D0FF89CE8B73A585A3265963AE39708' with your actual Steam API key
STEAM_API_KEY = '7D0FF89CE8B73A585A3265963AE39708'

STEAM_API_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'

def get_recent_playtime(steam_id):
    two_weeks_ago = int((datetime.now() - timedelta(days=14)).timestamp())

    params = {
        'key': STEAM_API_KEY,
        'steamid': steam_id,
        'format': 'json',
        'include_played_free_games': 1,
        'include_appinfo': 1,
        'include_free_sub': 1,
    }

    response = requests.get(STEAM_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        games = data['response']['games']

        # Filter out games with playtime equal to 0 or last played before two weeks ago
        games = [game for game in games if game['playtime_forever'] > 0 and game.get('playtime_2weeks', 0) > 0]

        return games
    else:
        print(f"Failed to fetch playtime data. Status code: {response.status_code}")
        return None


def plot_playtime_graph(steam_id):
    games = get_recent_playtime(steam_id)
    game_names = [game['name'] for game in games]
    playtimes = [game['playtime_2weeks'] // 60 for game in games]  # Corrected playtime calculation to use playtime_2weeks

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


