import json
import seaborn as sns
import matplotlib.pyplot as plt

# Load JSON data from file
with open('steam.json', 'r') as file:
    game_data = json.load(file)

# Get prices from the JSON data
game_prices = [game['price'] for game in game_data]


x_axis_range = (0, 60)


sns.histplot(game_prices, kde=True, bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Prices of All Games')
plt.xlabel('Price')
plt.ylabel('Number of games')
plt.xlim(x_axis_range)
plt.show()