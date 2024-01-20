import json
import statistics

ALL_GENRES = """All Possible Genres:
Accounting
Action
Adventure
Animation & Modeling
Audio Production
Casual
Design & Illustration
Documentary
Early Access
Education
Free to Play
Game Development
Gore
Indie
Massively Multiplayer
Nudity
Photo Editing
RPG
Racing
Sexual Content
Simulation
Software Training
Sports
Strategy
Tutorial
Utilities
Video Production
Violent
Web Publishing
"""

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def descriptive_stats_qualitative(data, variable):
    values = data[variable].split(';') if ';' in data[variable] else [data[variable]]
    result = {
        "variable": variable,
        "categories": values,
        "num_categories": len(values)
    }
    return result

def descriptive_stats_quantitative(data, variable):
    values = [data[variable]]  # Wrap the integer in a list
    result = {
        "variable": variable,
        "mean": statistics.mean(values),
        "median": statistics.median(values)
    }

    if len(values) >= 2:
        result["variance"] = statistics.variance(values)
        result["std_dev"] = statistics.stdev(values)
    else:
        result["variance"] = None
        result["std_dev"] = None

    return result

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

    result = []
    for i, game in enumerate(sorted_games[:n], start=1):
        positive_percentage = (game["positive_ratings"] / (game["positive_ratings"] + game["negative_ratings"])) * 100
        result.append({
            "rank": i,
            "name": game['name'],
            "positive_percentage": positive_percentage,
            "owners": game['owners']
        })

    return result

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
    result = top_games_in_genre(game_data, user_genre)
    for game in result:
        print(f"{game['rank']}. {game['name']} - Positive Percentage: {game['positive_percentage']:.2f}% - Owners: {game['owners']}")
        game_result = (f"{game['rank']}. {game['name']} - Positive Percentage: {game['positive_percentage']:.2f}% - Owners: {game['owners']}")