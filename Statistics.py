import json
import statistics

# print("""All Possible Genres:
# Action
# Adventure
# Animation & Modeling
# Casual
# Design & Illustration
# Education
# Indie
# Massively Multiplayer
# RPG
# Racing
# Simulation
# Software Training
# Strategy
# Utilities
# Video Production
# Violent
# Web Publishing
# """)


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def top_games_in_genre(data, genre, int_owners=50000, n=5):
    genre_lower = genre.lower()
    genre_games = [game for game in data if
                   genre_lower in game["genres"].lower().split(';') and
                   game["positive_ratings"] + game["negative_ratings"] > 0 and
                   game["positive_ratings"] < game["positive_ratings"] + game["negative_ratings"] and
                   int(game["owners"].split('-')[0]) >= int_owners]
    sorted_games = sorted(genre_games,
                          key=lambda x: x["positive_ratings"] / (x["positive_ratings"] + x["negative_ratings"]),
                          reverse=True)

    array = []
    for i, game in enumerate(sorted_games[:n], start=1):
        positive_percentage = (game["positive_ratings"] / (game["positive_ratings"] + game["negative_ratings"])) * 100
        array.append(f"{i}. {game['name']} - Positive Percentage: {positive_percentage:.2f}%")
    return array


if __name__ == "__main__":
    file_path = "steam.json"
    game_data = read_json_file(file_path)

    for entry in game_data:
        owners = entry.get("owners")

        owners_range = owners.split('-')
        if len(owners_range) == 2:
            int_owners = int(owners_range[0])
        else:
            int_owners = int(owners)

        if int_owners >= 100000:
            int_owners = 50000

    user_genre = input("\nEnter a genre to find the top 5 games (case-insensitive): ")
    top_games_in_genre(game_data, user_genre)

