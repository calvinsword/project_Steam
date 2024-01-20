
import requests
from bs4 import BeautifulSoup


def get_steam_game_info_by_name(game_name):
    search_url = f'https://store.steampowered.com/search/?term={game_name}'

    try:
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            first_result = soup.find('a', {'class': 'search_result_row'})

            if first_result:
                title = first_result.find('span', {'class': 'title'}).text.strip()
                url = first_result['href']

                return url
            else:
                return None
        else:
            return {'error': f'Unable to fetch the page. Status Code: {response.status_code}'}

    except Exception as e:
        return {'error': str(e)}
