import requests
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SteamDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Steam Dashboard")
        self.geometry("800x600")


        self.api_key = '7D0FF89CE8B73A585A3265963AE39708'
        self.user_id = '76561199005826631'

        # Fetch data from Steam API and limit to top 30 games
        self.steam_data = self.get_steam_data()[:30]

        # Sort data using quicksort
        self.sorted_data = self.quicksort(self.steam_data, key=lambda x: x['playtime_forever'], reverse=True)

        # Plot playtime distribution
        self.plot_playtime_distribution()

        # Create UI components
        self.create_widgets()

    def get_steam_data(self):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.api_key}&steamid={self.user_id}"
        response = requests.get(url)
        data = response.json()
        return data["response"]["games"]

    def quicksort(self, data, key=lambda x: x['name'], reverse=False):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if key(x) < key(pivot)]
        middle = [x for x in data if key(x) == key(pivot)]
        right = [x for x in data if key(x) > key(pivot)]
        return self.quicksort(left, key, reverse) + middle + self.quicksort(right, key, reverse)

    def plot_playtime_distribution(self):
        playtimes = [game['playtime_forever'] for game in self.steam_data]
        plt.hist(playtimes, bins=20, color='blue', edgecolor='black')
        plt.xlabel('Playtime (minutes)')
        plt.ylabel('Frequency')
        plt.title('Playtime Distribution')
        plt.savefig('playtime_distribution.png')

    def create_widgets(self):
        # Display Sorted Data
        sorted_data_label = tk.Label(self, text="Top 30 Games by Playtime")
        sorted_data_label.pack()

        sorted_data_treeview = ttk.Treeview(self, columns=('Name', 'Playtime'))
        sorted_data_treeview.heading('Name', text='Name')
        sorted_data_treeview.heading('Playtime', text='Playtime (minutes)')

        for game in self.sorted_data:
            try:
                name = game.get('name') or game.get('title') or 'Unknown Game'
                playtime = game.get('playtime_forever', 'Unknown Playtime')

                # Fallback to 'appid' if 'name' is not available
                if name == 'Unknown Game':
                    name = self.get_game_name(game.get('appid', 'Unknown Game'))

                sorted_data_treeview.insert('', 'end', values=(name, playtime))
            except Exception as e:
                print(f"Error processing data for game: {e}")
                print(f"Full game data: {game}")

        sorted_data_treeview.pack()

        # Display Playtime Distribution
        playtime_distribution_label = tk.Label(self, text="Playtime Distribution")
        playtime_distribution_label.pack()

        # Embed Matplotlib plot in Tkinter
        playtime_distribution_image = tk.PhotoImage(file='playtime_distribution.png')
        canvas = tk.Canvas(self, width=600, height=400)
        canvas.create_image(0, 0, anchor='nw', image=playtime_distribution_image)
        canvas.pack()

    def get_game_name(self, appid):
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful and data is available
        if response.status_code == 200 and data.get(str(appid), {}).get('success', False):
            return data[str(appid)]['data'].get('name', 'Unknown Game')
        else:
            return 'Unknown Game'

if __name__ == "__main__":
    app = SteamDashboard()
    app.mainloop()