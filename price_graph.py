import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Lees de data uit het JSON-bestand
with open('steam.json', 'r') as file:
    data = json.load(file)

# Verzamel de relevante gegevens (price en median_playtime)
prices = []
playtimes = []
for game in data:
    prices.append(game['price'])
    playtimes.append(game['median_playtime'])

# Converteer naar numpy-arrays
X = np.array(prices).reshape(-1, 1)
y = np.array(playtimes)

# Verdeel de data in trainings- en testsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Maak een lineaire regressie model
model = LinearRegression()
model.fit(X_train, y_train)

# Voorspel de y-waarden voor de testset
y_pred = model.predict(X_test)

# Plot the results with reversed axes
plt.scatter(X_test, y_test, color='black', label='Test data')  # Swap X_test and y_test
plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Linear regression')  # Swap X_test and y_pred
plt.title('Linear Regression: Median Playtime vs. Price')
plt.xlabel('Price')  # Swap labels
plt.ylabel('Median Playtime (hours)')  # Swap labels

# Set the maximum limits
plt.xlim(0, 60)
plt.ylim(0, 4000)

plt.legend()
plt.savefig("Images/GamePrice.png")
plt.show()

