
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

                return {'title': title, 'url': url}
            else:
                return None
        else:
            print(f'Error: Unable to fetch the page. Status Code: {response.status_code}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None


game_name = input("Naam van het spel:")
game_info = get_steam_game_info_by_name(game_name)

if game_info:
    print(f"Title: {game_info['title']}")
    print(f"URL: {game_info['url']}")
else:
    print(f"No information found for the game '{game_name}'.")