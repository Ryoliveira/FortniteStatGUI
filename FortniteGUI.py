import tkinter
from PIL import ImageTk, Image
import configparser
import requests
import webbrowser

# Load configuration file with API keys
Config = configparser.ConfigParser()
Config.read('tokens.ini')
# Tracker Network
TRN_key = Config.get('Tokens', 'trn-api-key')
HEADERS = {'TRN-Api-Key': TRN_key}


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.player_stats = {}
        # Window settings
        self.title("Fortnite Stats")
        self.geometry('500x365')
        # self.resizable(False, False)
        self.configure(background='light grey')

        # Title Bar Frame
        title_bar_frame = tkinter.Frame(self)
        title_bar_frame.pack(fill='x')
        title_bar_frame.configure(background='purple')
        # Logo
        self.logo = ImageTk.PhotoImage(Image.open('fortnite-logo.png'))
        tkinter.Label(title_bar_frame, image=self.logo,  bg='purple').grid(row=0, column=0, rowspan=2)
        program_title = tkinter.Label(title_bar_frame, text='FORTNITE Stat Tracker', bg='purple')
        program_title.grid(row=0, column=1)
        program_title.configure(font=("Arial", 26, 'bold'))

        #API Credits
        api_credits = tkinter.Label(title_bar_frame, text='Powered By: Fortnitetracker.com', bg='purple')
        api_credits.grid(row=1, column=1)
        api_credits.configure(font=("Arial", 18, 'bold'))
        api_credits.bind("<Button-1>", self.tracker_page)
        #######################
        #   Lifetime Stats    #
        #######################
        # Stat frame
        stat_frame = tkinter.Frame(self)
        stat_frame.pack(fill='x')
        stat_frame.configure(bg='light blue')

        # Account label
        self.account_name = tkinter.StringVar()
        tkinter.Label(stat_frame, text='Account: ', font=('Arial', 12, "bold"), bg='light blue', fg='black').grid(row=0, column=0)
        tkinter.Label(stat_frame, textvariable=self.account_name, font=('bold', 12), bg='light blue', fg='black').grid(row=0, column=1, sticky='w')

        # Platform label
        self.platform = tkinter.StringVar()
        self.platform.set('PC')
        tkinter.Label(stat_frame, text='Platform: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=1, column=0)
        tkinter.Label(stat_frame, textvariable=self.platform, font=('bold', 12), bg='light blue', fg='black').grid(row=1, column=1, sticky='w')

        # Check Boxes
        tkinter.Checkbutton(stat_frame, text='Solo', bg='light blue', font=('Arial', 12, 'bold')).grid(row=0, column=2)
        tkinter.Checkbutton(stat_frame, text='Duo', bg='light blue', font=('Arial', 12, 'bold')).grid(row=0, column=3)
        tkinter.Checkbutton(stat_frame, text='Squad', bg='light blue', font=('Arial', 12, 'bold')).grid(row=0, column=4)

        # Lifetime title label
        tkinter.Label(stat_frame, text='==Lifetime Stats==', font=('Arial', 14, 'bold'), bg='light blue', fg='black').grid(row=2, column=1, columnspan=3, sticky='ew')

        # Win label
        self.wins = tkinter.StringVar()
        tkinter.Label(stat_frame, text='Wins: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=3, column=0, sticky='e')
        tkinter.Label(stat_frame, textvariable=self.wins, font=('Arial', 12), bg='light blue', fg='black').grid(row=3, column=1, sticky='w')

        # Matches Played Label
        self.matches_played = tkinter.StringVar()
        tkinter.Label(stat_frame, text='Matches Played: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=4, column=0, sticky='e')
        tkinter.Label(stat_frame, textvariable=self.matches_played, font=('Arial', 12), bg='light blue', fg='black').grid(row=4, column=1, sticky='w')

        # Win Percentage Label
        self.win_per = tkinter.StringVar()
        tkinter.Label(stat_frame, text='Win Percentage: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=5, column=0, sticky='e')
        tkinter.Label(stat_frame, textvariable=self.win_per, font=('Arial', 12), bg='light blue', fg='black').grid(row=5, column=1, sticky='w')

        # Kills Label
        self.kills = tkinter.StringVar()
        tkinter.Label(stat_frame, text='Kills: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=3, column=3, sticky='e')
        tkinter.Label(stat_frame, textvariable=self.kills, font=('Arial', 12), bg='light blue', fg='black').grid(row=3, column=4, sticky='w')

        # Kill/Death Ration Label0
        self.kdr = tkinter.StringVar()
        tkinter.Label(stat_frame, text='KDR: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=4, column=3, sticky='e')
        tkinter.Label(stat_frame, textvariable=self.kdr, font=('Arial', 12), bg='light blue', fg='black').grid(row=4, column=4, sticky='w')

        # Score Per Match Label
        self.spm = tkinter.StringVar()
        tkinter.Label(stat_frame, text='Avg. Score:', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=5, column=3, sticky='e')
        tkinter.Label(stat_frame, textvariable=self.spm, font=('Arial', 12), bg='light blue', fg='black').grid(row=5, column=4, sticky='w')
        #######################
        #   Seasonal Stats    #
        #######################
        # Season Stat frame
        season_stat_frame = tkinter.Frame(self)
        season_stat_frame.pack(fill='x')
        season_stat_frame.configure(bg='light blue')

        # Season Title label
        tkinter.Label(season_stat_frame, text='   ==Seasonal Stats==', font=('Arial', 14, 'bold'), bg='light blue', fg='black').grid(row=0, column=1, columnspan=3, sticky='ew')

        # Win label
        self.season_wins = tkinter.StringVar()
        tkinter.Label(season_stat_frame, text='Wins: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=1, column=0, sticky='e')
        tkinter.Label(season_stat_frame, textvariable=self.season_wins, font=('Arial', 12), bg='light blue', fg='black').grid(row=1, column=1, sticky='w')

        # Matches Played Label
        self.season_matches_played = tkinter.StringVar()
        tkinter.Label(season_stat_frame, text='Matches Played: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=2, column=0, sticky='e')
        tkinter.Label(season_stat_frame, textvariable=self.season_matches_played, font=('Arial', 12), bg='light blue', fg='black').grid(row=2, column=1, sticky='w')

        # Win Percentage Label
        self.season_win_per = tkinter.StringVar()
        tkinter.Label(season_stat_frame, text='Win Percentage: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=3, column=0, sticky='e')
        tkinter.Label(season_stat_frame, textvariable=self.season_win_per, font=('Arial', 12), bg='light blue', fg='black').grid(row=3, column=1, sticky='w')

        # Kills Label
        self.season_kills = tkinter.StringVar()
        tkinter.Label(season_stat_frame, text='Kills: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=1, column=3, sticky='e')
        tkinter.Label(season_stat_frame, textvariable=self.season_kills, font=('Arial', 12), bg='light blue', fg='black').grid(row=1, column=4, sticky='w')

        # Kill/Death Ration Label
        self.season_kdr = tkinter.StringVar()
        tkinter.Label(season_stat_frame, text='KDR: ', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=2, column=3, sticky='e')
        tkinter.Label(season_stat_frame, textvariable=self.season_kdr, font=('Arial', 12), bg='light blue', fg='black').grid(row=2, column=4, sticky='w')

        # Avg score per match
        self.season_spm = tkinter.StringVar()
        tkinter.Label(season_stat_frame, text='Avg. Score:', font=('Arial', 12, 'bold'), bg='light blue', fg='black').grid(row=3, column=3, sticky='e')
        tkinter.Label(season_stat_frame, textvariable=self.season_spm, font=('Arial', 12), bg='light blue', fg='black').grid(row=3, column=4, sticky='w')

        self.solo_player_stats()
        self.update()

    def solo_player_stats(self):
        """Grab lifetime/seasonal solo stats"""
        player_data = self.grab_player_profile()
        # Lifetime stats
        solo_stats = player_data['stats']['p2']
        self.account_name.set(player_data['epicUserHandle'])
        self.platform.set(player_data['platformNameLong'])
        self.matches_played.set(solo_stats['matches']['value'])
        self.wins.set(solo_stats['top1']['value'])
        self.win_per.set("%.2f" % ((solo_stats['top1']['valueInt'] / solo_stats['matches']['valueInt']) * 100) + "%")
        self.kills.set(solo_stats['kills']['value'])
        self.kdr.set(solo_stats['kd']['value'])
        self.spm.set(solo_stats['scorePerMatch']['value'])
        # Seasonal Stats
        season_solo_stats = player_data['stats']['curr_p2']
        self.season_matches_played.set(season_solo_stats['matches']['value'])
        self.season_wins.set(season_solo_stats['top1']['value'])
        self.season_win_per.set("%.2f" % ((season_solo_stats['top1']['valueInt'] / season_solo_stats['matches']['valueInt']) * 100) + "%")
        self.season_kills.set(season_solo_stats['kills']['value'])
        self.season_kdr.set(season_solo_stats['kd']['value'])
        self.season_spm.set(season_solo_stats['scorePerMatch']['value'])

    def duo_player_stats(self):
        """Grab lifetime/seasonal duo stats"""
        player_data = self.grab_player_profile()
        # Lifetime stats
        duo_stats = player_data['stats']['p10']
        self.account_name.set(player_data['epicUserHandle'])
        self.platform.set(player_data['platformNameLong'])
        self.matches_played.set(duo_stats['matches']['value'])
        self.wins.set(duo_stats['top1']['value'])
        self.win_per.set("%.2f" % ((duo_stats['top1']['valueInt'] / duo_stats['matches']['valueInt']) * 100) + "%")
        self.kills.set(duo_stats['kills']['value'])
        self.kdr.set(duo_stats['kd']['value'])
        self.spm.set(duo_stats['scorePerMatch']['value'])
        # Seasonal Stats
        season_duo_stats = player_data['stats']['curr_p10']
        self.season_matches_played.set(season_duo_stats['matches']['value'])
        self.season_wins.set(season_duo_stats['top1']['value'])
        self.season_win_per.set("%.2f" % ((season_duo_stats['top1']['valueInt'] / season_duo_stats['matches']['valueInt']) * 100) + "%")
        self.season_kills.set(season_duo_stats['kills']['value'])
        self.season_kdr.set(season_duo_stats['kd']['value'])
        self.season_spm.set(season_duo_stats['scorePerMatch']['value'])

    def squad_player_stats(self):
        """Grab lifetime/seasonal squad stats"""
        player_data = self.grab_player_profile()
        # Lifetime stats
        squad_stats = player_data['stats']['p9']
        self.account_name.set(player_data['epicUserHandle'])
        self.platform.set(player_data['platformNameLong'])
        self.matches_played.set(squad_stats['matches']['value'])
        self.wins.set(squad_stats['top1']['value'])
        self.win_per.set("%.2f" % ((squad_stats['top1']['valueInt'] / squad_stats['matches']['valueInt']) * 100) + "%")
        self.kills.set(squad_stats['kills']['value'])
        self.kdr.set(squad_stats['kd']['value'])
        self.spm.set(squad_stats['scorePerMatch']['value'])
        # Seasonal Stats
        season_squad_stats = player_data['stats']['curr_p9']
        self.season_matches_played.set(season_squad_stats['matches']['value'])
        self.season_wins.set(season_squad_stats['top1']['value'])
        self.season_win_per.set("%.2f" % ((season_squad_stats['top1']['valueInt'] / season_squad_stats['matches']['valueInt']) * 100) + "%")
        self.season_kills.set(season_squad_stats['kills']['value'])
        self.season_kdr.set(season_squad_stats['kd']['value'])
        self.season_spm.set(season_squad_stats['scorePerMatch']['value'])

    def grab_player_profile(self):
        user = 'Rhyn091'
        platform = 'pc'
        r = requests.get('https://api.fortnitetracker.com/v1/profile/{}/{}'.format(platform, user), headers=HEADERS)
        player_data = r.json()
        return player_data

    def tracker_page(self, event):
        webbrowser.open_new(r"https://fortnitetracker.com/")

    def game_page(self, event):
        webbrowser.open_new(r"https://www.epicgames.com/fortnite/en-US/home")
if __name__ == '__main__':
    win = MainWindow()
    win.mainloop()



