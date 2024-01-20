import json
import statistics

print("""All Possible Genres:
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
""")


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def descriptive_stats_qualitative(data, variable):
    values = data[variable].split(';') if ';' in data[variable] else [data[variable]]
    print(f"Descriptive statistics for qualitative variable '{variable}':")
    print(f"Categories: {', '.join(values)}")
    print(f"Number of categories: {len(values)}")


def descriptive_stats_quantitative(data, variable):
    values = [data[variable]]  # Wrap the integer in a list
    print(f"\nDescriptive statistics for quantitative variable '{variable}':")
    print(f"Mean: {statistics.mean(values)}")
    print(f"Median: {statistics.median(values)}")

    if len(values) >= 2:
        print(f"Variance: {statistics.variance(values)}")
        print(f"Standard Deviation: {statistics.stdev(values)}")
    else:
        print("Variance and Standard Deviation cannot be calculated with a single data point.")


def top_games_in_genre(data, genre, int_owners=50000, n=5):
    genre_lower = genre.lower()
    genre_games = [game for game in data if
                   genre_lower in game["genres"].lower().split(';') and
                   game["positive_ratings"] + game["negative_ratings"] > 0 and
                   game["positive_ratings"] < game["positive_ratings"] + game["negative_ratings"] and
                   int(game["owners"].split('-')[
                           0]) >= int_owners]  # Skip games with 100% positive rating and less than 50,000 owners
    sorted_games = sorted(genre_games,
                          key=lambda x: x["positive_ratings"] / (x["positive_ratings"] + x["negative_ratings"]),
                          reverse=True)

    print(f"\nTop {n} games in the genre '{genre}' with at least {int_owners} owners based on % of positive ratings:")
    for i, game in enumerate(sorted_games[:n], start=1):
        positive_percentage = (game["positive_ratings"] / (game["positive_ratings"] + game["negative_ratings"])) * 100
        print(f"{i}. {game['name']} - Positive Percentage: {positive_percentage:.2f}% - Owners: {game['owners']}")


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
