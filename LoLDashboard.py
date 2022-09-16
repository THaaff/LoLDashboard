# imports
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly_express as px
import plotly.graph_objects as go

# request responses from urls and get tables
url_na = 'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?MHG%5Btournament%5D=LCS%2F2022+Season%2FSummer+Season&MHG%5Blimit%5D=1000&MHG%5Btextonly%5D=Yes&MHG%5Bpreload%5D=Tournament&MHG%5Bspl%5D=yes&_run='
response_na = requests.get(url_na)
soup_na = BeautifulSoup(response_na.text, 'html.parser')
na_table = soup_na.find('table')
url_eu = 'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?MHG%5Btournament%5D=LEC%2F2022+Season%2FSummer+Season&MHG%5Blimit%5D=1000&MHG%5Btextonly%5D=Yes&MHG%5Bpreload%5D=Tournament&MHG%5Bspl%5D=yes&_run='
response_eu = requests.get(url_eu)
soup_eu = BeautifulSoup(response_eu.text, 'html.parser')
eu_table = soup_eu.find('table')
url_cn = 'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?MHG%5Btournament%5D=LPL%2F2022+Season%2FSummer+Season&MHG%5Blimit%5D=1000&MHG%5Btextonly%5D=Yes&MHG%5Bpreload%5D=Tournament&MHG%5Bspl%5D=yes&_run='
response_cn = requests.get(url_cn)
soup_cn = BeautifulSoup(response_cn.text, 'html.parser')
cn_table = soup_cn.find('table')
url_kr = 'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D=LCK%2F2022+Season%2FSummer+Season&MHG%5Btextonly%5D=Yes&MHG%5Blimit%5D=1000&MHG%5Bspl%5D=yes&_run='
response_kr = requests.get(url_kr)
soup_kr = BeautifulSoup(response_kr.text, 'html.parser')
kr_table = soup_kr.find('table')

# scrape and set up dataframes
teams = ['100 Thieves', 'Cloud9', 'Counter Logic Gaming', 'Dignitas', 'Evil Geniuses.NA', 'FlyQuest', 'Golden Guardians', 'Immortals', 'Team Liquid', 'TSM', 'Astralis', 'Excel Esports', 'Fnatic', 'G2 Esports', 'MAD Lions', 'Misfits Gaming', 'Rogue (European Team)', 'SK Gaming', 'Team BDS', 'Team Vitality', "Anyone's Legend", 'Bilibili Gaming', 'EDward Gaming', 'FunPlus Phoenix', 'Invictus Gaming', 'JD Gaming', 'LGD Gaming', 'LNG Esports', 'Oh My God', 'Rare Atom', 'Royal Never Give Up', 'Team WE', 'ThunderTalk Gaming', 'Top Esports', 'Ultra Prime', 'Victory Five', 'Weibo Gaming', 'DRX', 'DWG KIA', 'Fredit BRION', 'Gen.G', 'Hanwha Life Esports', 'KT Rolster', 'Kwangdong Freecs', 'Liiv SANDBOX', 'Nongshim RedForce', 'T1']
tournament = ['LCS', 'LCS', 'LCS', 'LCS', 'LCS', 'LCS', 'LCS', 'LCS', 'LCS', 'LCS', 'LEC', 'LEC', 'LEC', 'LEC', 'LEC', 'LEC', 'LEC', 'LEC', 'LEC', 'LEC', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LPL', 'LCK', 'LCK', 'LCK', 'LCK', 'LCK', 'LCK', 'LCK', 'LCK', 'LCK', 'LCK',]
games_played = [0] * len(teams)
wins = [0] * len(teams)
losses = [0] * len(teams)
avg_game_length = [0] * len(teams)
avg_gold_per_minute = [0] * len(teams)
kills_per_game = [0] * len(teams)
towers_per_game = [0] * len(teams)
drakes_per_game = [0] * len(teams)
barons_per_game = [0] * len(teams)
heralds_per_game = [0] * len(teams)
champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol', 'Azir', 'Bard', "Bel'Veth", 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', "Cho'Gath", 'Corki', 'Darius', 'Diana', 'Dr. Mundo', 'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', "Kai'Sa", 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix", 'Kindred', 'Kled', "Kog'Maw", 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu', 'Nilah', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', "Rek'Sai", 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', "Vel'Koz", 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
total_played = [0] * len(champions)
total_banned = [0] * len(champions)
total_won = [0] * len(champions)
lcs_played = [0] * len(champions)
lcs_banned = [0] * len(champions)
lcs_won = [0] * len(champions)
lec_played = [0] * len(champions)
lec_banned = [0] * len(champions)
lec_won = [0] * len(champions)
lpl_played = [0] * len(champions)
lpl_banned = [0] * len(champions)
lpl_won = [0] * len(champions)
lck_played = [0] * len(champions)
lck_banned = [0] * len(champions)
lck_won = [0] * len(champions)
teams_dict = {'Team': teams, 'Tournament': tournament, 'Games_Played': games_played, 'Wins': wins, 'Losses': losses, 'Avg_Game_Length_Seconds': avg_game_length, 'Avg_Gold_per_Minute': avg_gold_per_minute, 'Kills_per_Game': kills_per_game, 'Towers_per_Game': towers_per_game, 'Drakes_per_Game': drakes_per_game, 'Barons_per_Game': barons_per_game, 'Heralds_per_Game': heralds_per_game}
games_dict = {'Date': [], 'Tournament': [], 'Patch': [], 'Blue': [], 'Red': [], 'Winner': [], 'Winner_Side': [], 'Blue_Bans': [], 'Red_Bans': [], 'Blue_Picks': [], 'Red_Picks': [], 'Game_Length': [], 'Blue_Gold': [], 'Blue_Kills': [], 'Blue_Towers': [], 'Blue_Drakes': [], 'Blue_Barons': [], 'Blue_Heralds': [], 'Red_Gold': [], 'Red_Kills': [], 'Red_Towers': [], 'Red_Drakes': [], 'Red_Barons': [], 'Red_Heralds': []}
champions_dict = {'Champion': champions, 'Total_Played': total_played, 'Total_Banned': total_banned, 'Total_Won': total_won, 'LCS_Played': lcs_played, 'LCS_Banned': lcs_banned, 'LCS_Won': lcs_won, 'LEC_Played': lec_played, 'LEC_Banned': lec_banned, 'LEC_Won': lec_won, 'LPL_Played': lpl_played, 'LPL_Banned': lpl_banned, 'LPL_Won': lpl_won, 'LCK_Played': lck_played, 'LCK_Banned': lck_banned, 'LCK_Won': lck_won}
teams_df = pd.DataFrame(teams_dict).set_index('Team')
champions_df = pd.DataFrame(champions_dict).set_index('Champion')
for rows in na_table.find_all('tr')[3:]:
    row = rows.find_all('td')
    games_dict['Tournament'].append('LCS')
    games_dict['Date'].append(datetime.strptime(row[0].get_text()[:10], '%Y-%m-%d').strftime('%m/%d'))
    blue = row[2].get_text()
    red = row[3].get_text()
    games_dict['Patch'].append(row[1].get_text())
    games_dict['Blue'].append(blue)
    games_dict['Red'].append(red)
    games_dict['Winner'].append(row[4].get_text())
    blue_picks = row[7].get_text().split(',')
    red_picks = row[8].get_text().split(',')
    games_dict['Blue_Picks'].append(blue_picks)
    games_dict['Red_Picks'].append(red_picks)
    if row[4].get_text() == blue:
        games_dict['Winner_Side'].append('Blue')
        teams_df.loc[blue, 'Wins'] += 1
        teams_df.loc[red, 'Losses'] += 1
        for blue_pick in blue_picks:
            champions_df.loc[blue_pick, 'Total_Won'] += 1
            champions_df.loc[blue_pick, 'LCS_Won'] += 1
    else:
        games_dict['Winner_Side'].append('Red')
        teams_df.loc[red, 'Wins'] += 1
        teams_df.loc[blue, 'Losses'] += 1
        for red_pick in red_picks:
            champions_df.loc[red_pick, 'Total_Won'] += 1
            champions_df.loc[red_pick, 'LCS_Won'] += 1
    teams_df.loc[blue, 'Games_Played'] += 1
    teams_df.loc[red, 'Games_Played'] += 1
    picks = blue_picks + red_picks
    for pick in picks:
        champions_df.loc[pick, 'Total_Played'] += 1
        champions_df.loc[pick, 'LCS_Played'] += 1
    games_dict['Blue_Bans'].append(row[5].get_text())
    games_dict['Red_Bans'].append(row[6].get_text())
    bans = row[5].get_text().split(',') + row[6].get_text().split(',')
    for ban in bans:
        if ban != 'None':
            champions_df.loc[ban, 'Total_Banned'] += 1
            champions_df.loc[ban, 'LCS_Banned'] += 1
    games_dict['Game_Length'].append(row[11].get_text())
    teams_df.loc[blue, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    teams_df.loc[red, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    games_dict['Blue_Gold'].append(int(row[12].get_text()))
    games_dict['Red_Gold'].append(int(row[18].get_text()))
    teams_df.loc[blue, 'Avg_Gold_per_Minute'] += int(row[12].get_text())
    teams_df.loc[red, 'Avg_Gold_per_Minute'] += int(row[18].get_text())
    games_dict['Blue_Kills'].append(int(row[13].get_text()))
    games_dict['Red_Kills'].append(int(row[19].get_text()))
    teams_df.loc[blue, 'Kills_per_Game'] += int(row[13].get_text())
    teams_df.loc[red, 'Kills_per_Game'] += int(row[19].get_text())
    games_dict['Blue_Towers'].append(int(row[14].get_text()))
    games_dict['Red_Towers'].append(int(row[20].get_text()))
    teams_df.loc[blue, 'Towers_per_Game'] += int(row[14].get_text())
    teams_df.loc[red, 'Towers_per_Game'] += int(row[20].get_text())
    games_dict['Blue_Drakes'].append(int(row[15].get_text()))
    games_dict['Red_Drakes'].append(int(row[21].get_text()))
    teams_df.loc[blue, 'Drakes_per_Game'] += int(row[15].get_text())
    teams_df.loc[red, 'Drakes_per_Game'] += int(row[21].get_text())
    games_dict['Blue_Barons'].append(int(row[16].get_text()))
    games_dict['Red_Barons'].append(int(row[22].get_text()))
    teams_df.loc[blue, 'Barons_per_Game'] += int(row[16].get_text())
    teams_df.loc[red, 'Barons_per_Game'] += int(row[22].get_text())
    games_dict['Blue_Heralds'].append(int(row[17].get_text()))
    games_dict['Red_Heralds'].append(int(row[23].get_text()))
    teams_df.loc[blue, 'Heralds_per_Game'] += int(row[17].get_text())
    teams_df.loc[red, 'Heralds_per_Game'] += int(row[23].get_text())
for rows in eu_table.find_all('tr')[3:]:
    row = rows.find_all('td')
    games_dict['Tournament'].append('LEC')
    games_dict['Date'].append(datetime.strptime(row[0].get_text()[:10], '%Y-%m-%d').strftime('%m/%d'))
    blue = row[2].get_text()
    red = row[3].get_text()
    games_dict['Patch'].append(row[1].get_text())
    games_dict['Blue'].append(blue)
    games_dict['Red'].append(red)
    games_dict['Winner'].append(row[4].get_text())
    blue_picks = row[7].get_text().split(',')
    red_picks = row[8].get_text().split(',')
    games_dict['Blue_Picks'].append(blue_picks)
    games_dict['Red_Picks'].append(red_picks)
    if row[4].get_text() == blue:
        games_dict['Winner_Side'].append('Blue')
        teams_df.loc[blue, 'Wins'] += 1
        teams_df.loc[red, 'Losses'] += 1
        for blue_pick in blue_picks:
            champions_df.loc[blue_pick, 'Total_Won'] += 1
            champions_df.loc[blue_pick, 'LEC_Won'] += 1
    else:
        games_dict['Winner_Side'].append('Red')
        teams_df.loc[red, 'Wins'] += 1
        teams_df.loc[blue, 'Losses'] += 1
        for red_pick in red_picks:
            champions_df.loc[red_pick, 'Total_Won'] += 1
            champions_df.loc[red_pick, 'LEC_Won'] += 1
    teams_df.loc[blue, 'Games_Played'] += 1
    teams_df.loc[red, 'Games_Played'] += 1
    picks = blue_picks + red_picks
    for pick in picks:
        champions_df.loc[pick, 'Total_Played'] += 1
        champions_df.loc[pick, 'LEC_Played'] += 1
    games_dict['Blue_Bans'].append(row[5].get_text())
    games_dict['Red_Bans'].append(row[6].get_text())
    bans = row[5].get_text().split(',') + row[6].get_text().split(',')
    for ban in bans:
        if ban != 'None':
            champions_df.loc[ban, 'Total_Banned'] += 1
            champions_df.loc[ban, 'LEC_Banned'] += 1
    games_dict['Game_Length'].append(row[11].get_text())
    teams_df.loc[blue, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    teams_df.loc[red, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    games_dict['Blue_Gold'].append(int(row[12].get_text()))
    games_dict['Red_Gold'].append(int(row[18].get_text()))
    teams_df.loc[blue, 'Avg_Gold_per_Minute'] += int(row[12].get_text())
    teams_df.loc[red, 'Avg_Gold_per_Minute'] += int(row[18].get_text())
    games_dict['Blue_Kills'].append(int(row[13].get_text()))
    games_dict['Red_Kills'].append(int(row[19].get_text()))
    teams_df.loc[blue, 'Kills_per_Game'] += int(row[13].get_text())
    teams_df.loc[red, 'Kills_per_Game'] += int(row[19].get_text())
    games_dict['Blue_Towers'].append(int(row[14].get_text()))
    games_dict['Red_Towers'].append(int(row[20].get_text()))
    teams_df.loc[blue, 'Towers_per_Game'] += int(row[14].get_text())
    teams_df.loc[red, 'Towers_per_Game'] += int(row[20].get_text())
    games_dict['Blue_Drakes'].append(int(row[15].get_text()))
    games_dict['Red_Drakes'].append(int(row[21].get_text()))
    teams_df.loc[blue, 'Drakes_per_Game'] += int(row[15].get_text())
    teams_df.loc[red, 'Drakes_per_Game'] += int(row[21].get_text())
    games_dict['Blue_Barons'].append(int(row[16].get_text()))
    games_dict['Red_Barons'].append(int(row[22].get_text()))
    teams_df.loc[blue, 'Barons_per_Game'] += int(row[16].get_text())
    teams_df.loc[red, 'Barons_per_Game'] += int(row[22].get_text())
    games_dict['Blue_Heralds'].append(int(row[17].get_text()))
    games_dict['Red_Heralds'].append(int(row[23].get_text()))
    teams_df.loc[blue, 'Heralds_per_Game'] += int(row[17].get_text())
    teams_df.loc[red, 'Heralds_per_Game'] += int(row[23].get_text())
for rows in cn_table.find_all('tr')[3:]:
    row = rows.find_all('td')
    games_dict['Tournament'].append('LPL')
    games_dict['Date'].append(datetime.strptime(row[0].get_text()[:10], '%Y-%m-%d').strftime('%m/%d'))
    blue = row[2].get_text()
    red = row[3].get_text()
    games_dict['Patch'].append(row[1].get_text())
    games_dict['Blue'].append(blue)
    games_dict['Red'].append(red)
    games_dict['Winner'].append(row[4].get_text())
    blue_picks = row[7].get_text().split(',')
    red_picks = row[8].get_text().split(',')
    games_dict['Blue_Picks'].append(blue_picks)
    games_dict['Red_Picks'].append(red_picks)
    if row[4].get_text() == blue:
        games_dict['Winner_Side'].append('Blue')
        teams_df.loc[blue, 'Wins'] += 1
        teams_df.loc[red, 'Losses'] += 1
        for blue_pick in blue_picks:
            champions_df.loc[blue_pick, 'Total_Won'] += 1
            champions_df.loc[blue_pick, 'LPL_Won'] += 1
    else:
        games_dict['Winner_Side'].append('Red')
        teams_df.loc[red, 'Wins'] += 1
        teams_df.loc[blue, 'Losses'] += 1
        for red_pick in red_picks:
            champions_df.loc[red_pick, 'Total_Won'] += 1
            champions_df.loc[red_pick, 'LPL_Won'] += 1
    teams_df.loc[blue, 'Games_Played'] += 1
    teams_df.loc[red, 'Games_Played'] += 1
    picks = blue_picks + red_picks
    for pick in picks:
        champions_df.loc[pick, 'Total_Played'] += 1
        champions_df.loc[pick, 'LPL_Played'] += 1
    games_dict['Blue_Bans'].append(row[5].get_text())
    games_dict['Red_Bans'].append(row[6].get_text())
    bans = row[5].get_text().split(',') + row[6].get_text().split(',')
    for ban in bans:
        if ban != 'None':
            champions_df.loc[ban, 'Total_Banned'] += 1
            champions_df.loc[ban, 'LPL_Banned'] += 1
    games_dict['Game_Length'].append(row[11].get_text())
    teams_df.loc[blue, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    teams_df.loc[red, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    games_dict['Blue_Gold'].append(int(row[12].get_text()))
    games_dict['Red_Gold'].append(int(row[18].get_text()))
    teams_df.loc[blue, 'Avg_Gold_per_Minute'] += int(row[12].get_text())
    teams_df.loc[red, 'Avg_Gold_per_Minute'] += int(row[18].get_text())
    games_dict['Blue_Kills'].append(int(row[13].get_text()))
    games_dict['Red_Kills'].append(int(row[19].get_text()))
    teams_df.loc[blue, 'Kills_per_Game'] += int(row[13].get_text())
    teams_df.loc[red, 'Kills_per_Game'] += int(row[19].get_text())
    games_dict['Blue_Towers'].append(int(row[14].get_text()))
    games_dict['Red_Towers'].append(int(row[20].get_text()))
    teams_df.loc[blue, 'Towers_per_Game'] += int(row[14].get_text())
    teams_df.loc[red, 'Towers_per_Game'] += int(row[20].get_text())
    games_dict['Blue_Drakes'].append(int(row[15].get_text()))
    games_dict['Red_Drakes'].append(int(row[21].get_text()))
    teams_df.loc[blue, 'Drakes_per_Game'] += int(row[15].get_text())
    teams_df.loc[red, 'Drakes_per_Game'] += int(row[21].get_text())
    games_dict['Blue_Barons'].append(int(row[16].get_text()))
    games_dict['Red_Barons'].append(int(row[22].get_text()))
    teams_df.loc[blue, 'Barons_per_Game'] += int(row[16].get_text())
    teams_df.loc[red, 'Barons_per_Game'] += int(row[22].get_text())
    # at time of programming: lol.fandom's query form for lpl games does not show rift heralds 
    games_dict['Blue_Heralds'].append('N/A') # remove and include below if/when fixed
    games_dict['Red_Heralds'].append('N/A') # remove and include below if/when fixed
    #games_dict['Blue_Heralds'].append(int(row[17].get_text()))
    #games_dict['Red_Heralds'].append(int(row[23].get_text()))
    #teams_df.loc[blue, 'Heralds_per_Game'] += int(row[17].get_text())
    #teams_df.loc[red, 'Heralds_per_Game'] += int(row[23].get_text())
for rows in kr_table.find_all('tr')[3:]:
    row = rows.find_all('td')
    games_dict['Tournament'].append('LCK')
    games_dict['Date'].append(datetime.strptime(row[0].get_text()[:10], '%Y-%m-%d').strftime('%m/%d'))
    blue = row[2].get_text()
    red = row[3].get_text()
    games_dict['Patch'].append(row[1].get_text())
    games_dict['Blue'].append(blue)
    games_dict['Red'].append(red)
    games_dict['Winner'].append(row[4].get_text())
    blue_picks = row[7].get_text().split(',')
    red_picks = row[8].get_text().split(',')
    games_dict['Blue_Picks'].append(blue_picks)
    games_dict['Red_Picks'].append(red_picks)
    if row[4].get_text() == blue:
        games_dict['Winner_Side'].append('Blue')
        teams_df.loc[blue, 'Wins'] += 1
        teams_df.loc[red, 'Losses'] += 1
        for blue_pick in blue_picks:
            champions_df.loc[blue_pick, 'Total_Won'] += 1
            champions_df.loc[blue_pick, 'LCK_Won'] += 1
    else:
        games_dict['Winner_Side'].append('Red')
        teams_df.loc[red, 'Wins'] += 1
        teams_df.loc[blue, 'Losses'] += 1
        for red_pick in red_picks:
            champions_df.loc[red_pick, 'Total_Won'] += 1
            champions_df.loc[red_pick, 'LCK_Won'] += 1
    teams_df.loc[blue, 'Games_Played'] += 1
    teams_df.loc[red, 'Games_Played'] += 1
    picks = blue_picks + red_picks
    for pick in picks:
        champions_df.loc[pick, 'Total_Played'] += 1
        champions_df.loc[pick, 'LCK_Played'] += 1
    games_dict['Blue_Bans'].append(row[5].get_text())
    games_dict['Red_Bans'].append(row[6].get_text())
    bans = row[5].get_text().split(',') + row[6].get_text().split(',')
    for ban in bans:
        if ban != 'None':
            champions_df.loc[ban, 'Total_Banned'] += 1
            champions_df.loc[ban, 'LCK_Banned'] += 1
    games_dict['Game_Length'].append(row[11].get_text())
    teams_df.loc[blue, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    teams_df.loc[red, 'Avg_Game_Length_Seconds'] += float(row[11].get_text().split(':')[0]) * 60 + float(row[11].get_text().split(':')[1])
    games_dict['Blue_Gold'].append(int(row[12].get_text()))
    games_dict['Red_Gold'].append(int(row[18].get_text()))
    teams_df.loc[blue, 'Avg_Gold_per_Minute'] += int(row[12].get_text())
    teams_df.loc[red, 'Avg_Gold_per_Minute'] += int(row[18].get_text())
    games_dict['Blue_Kills'].append(int(row[13].get_text()))
    games_dict['Red_Kills'].append(int(row[19].get_text()))
    teams_df.loc[blue, 'Kills_per_Game'] += int(row[13].get_text())
    teams_df.loc[red, 'Kills_per_Game'] += int(row[19].get_text())
    games_dict['Blue_Towers'].append(int(row[14].get_text()))
    games_dict['Red_Towers'].append(int(row[20].get_text()))
    teams_df.loc[blue, 'Towers_per_Game'] += int(row[14].get_text())
    teams_df.loc[red, 'Towers_per_Game'] += int(row[20].get_text())
    games_dict['Blue_Drakes'].append(int(row[15].get_text()))
    games_dict['Red_Drakes'].append(int(row[21].get_text()))
    teams_df.loc[blue, 'Drakes_per_Game'] += int(row[15].get_text())
    teams_df.loc[red, 'Drakes_per_Game'] += int(row[21].get_text())
    games_dict['Blue_Barons'].append(int(row[16].get_text()))
    games_dict['Red_Barons'].append(int(row[22].get_text()))
    teams_df.loc[blue, 'Barons_per_Game'] += int(row[16].get_text())
    teams_df.loc[red, 'Barons_per_Game'] += int(row[22].get_text())
    games_dict['Blue_Heralds'].append(int(row[17].get_text()))
    games_dict['Red_Heralds'].append(int(row[23].get_text()))
    teams_df.loc[blue, 'Heralds_per_Game'] += int(row[17].get_text())
    teams_df.loc[red, 'Heralds_per_Game'] += int(row[23].get_text())
games_df = pd.DataFrame(games_dict)

# calculate average stats and win pct for each team, pick/ban pct for each champion in each region
teams_df['Avg_Gold_per_Minute'] = round((teams_df['Avg_Gold_per_Minute'])/((teams_df['Avg_Game_Length_Seconds'])/60))
#teams_df['Avg_Game_Length'] = str((teams_df['Avg_Game_Length_Seconds']/(teams_df['Games_Played']))//60) + ':' + str(((teams_df['Avg_Game_Length_Seconds'])/(teams_df['Games_Played']))%60)[:2]
teams_df['Avg_Game_Length_Minutes'] = round((teams_df['Avg_Game_Length_Seconds']/60)/(teams_df['Games_Played']), 2)
teams_df['Kills_per_Game'] = round(teams_df['Kills_per_Game']/(teams_df['Games_Played']), 2)
teams_df['Towers_per_Game'] = round(teams_df['Towers_per_Game']/(teams_df['Games_Played']), 2)
teams_df['Drakes_per_Game'] = round(teams_df['Drakes_per_Game']/(teams_df['Games_Played']), 2)
teams_df['Barons_per_Game'] = round(teams_df['Barons_per_Game']/(teams_df['Games_Played']), 2)
teams_df['Heralds_per_Game'] = round(teams_df['Heralds_per_Game']/(teams_df['Games_Played']), 2)
teams_df['Objectives_per_Game'] = round(teams_df['Towers_per_Game'] + teams_df['Drakes_per_Game'] + teams_df['Barons_per_Game'], 2)
# delete line above and include line below if/when lpl rift heralds are shown
#teams_df['Objectives_per_Game'] = teams_df['Towers_per_Game'] + teams_df['Drakes_per_Game'] + teams_df['Barons_per_Game'] + teams_df['Heralds_per_Game']
teams_df['Win_Pct'] = round(teams_df['Wins']/teams_df['Games_Played'], 4)
champions_df['Ovr_PickBan_Pct'] = round((champions_df['Total_Played'] + champions_df['Total_Banned']) / len(games_df), 4)
champions_df['LCS_PickBan_Pct'] = round((champions_df['LCS_Played'] + champions_df['LCS_Banned']) / len(games_df[games_df.Tournament == 'LCS']), 4)
champions_df['LEC_PickBan_Pct'] = round((champions_df['LEC_Played'] + champions_df['LEC_Banned']) / len(games_df[games_df.Tournament == 'LEC']), 4)
champions_df['LPL_PickBan_Pct'] = round((champions_df['LPL_Played'] + champions_df['LPL_Banned']) / len(games_df[games_df.Tournament == 'LPL']), 4)
champions_df['LCK_PickBan_Pct'] = round((champions_df['LCK_Played'] + champions_df['LCK_Banned']) / len(games_df[games_df.Tournament == 'LCK']), 4)

teams_df = teams_df.reset_index()
teams_df.loc[4, 'Team'] = 'Evil Geniuses'
teams_df.loc[16, 'Team'] = 'Rogue'
champions_df = champions_df.reset_index()
display_champions_df = champions_df[(champions_df.Total_Played > 0) & (champions_df.Total_Banned > 0)].sort_values(by='Ovr_PickBan_Pct', ascending=False)
display_games_df = games_df.sort_values(by='Date', ascending=False)

# function to display data in dashboard
def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# dashboard
app = dash.Dash(__name__,)

fig = go.Figure()
fig.add_trace(go.Histogram(histfunc='avg', x = teams_df['Tournament'], y = teams_df['Avg_Game_Length_Minutes'], name='Game Length'))
fig.add_trace(go.Histogram(histfunc='avg', x = teams_df['Tournament'], y = teams_df['Kills_per_Game'], name='Kills per Game'))
fig.update_traces(hovertemplate = '%{y:.2f}')
fig.update_layout(title_text='Average Game Length and Kills per Game by Region', xaxis_title_text='Region', yaxis_title_text='Minutes/Kills', hovermode='x unified')

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Regional Differences', children=[
            html.H2('Average Game Length and Kills per Game Across Regions'),
            dcc.Graph(figure=fig),
            html.Br(),
            html.H2('Champion and Side Preferences Across Regions'),
            dcc.Dropdown(
                id='region-dropdown-tab-1',
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'North America (LCS)', 'value': 'LCS'},
                    {'label': 'Europe (LEC)', 'value': 'LEC'},
                    {'label': 'China (LPL)', 'value': 'LPL'},
                    {'label': 'South Korea (LCK)', 'value': 'LCK'},
                ],
                value='All',
                placeholder='All'
            ),
            dcc.Graph(id='champion-pb-rate'),
            dcc.Graph(id='winner-side-pct')
        ]),
        dcc.Tab(label='Top Teams', children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label('Region'),
                                dcc.Dropdown(
                                    id='region-dropdown-tab-2',
                                    options=[
                                        {'label': 'All', 'value': 'All'},
                                        {'label': 'North America (LCS)', 'value': 'LCS'},
                                        {'label': 'Europe (LEC)', 'value': 'LEC'},
                                        {'label': 'China (LPL)', 'value': 'LPL'},
                                        {'label': 'South Korea (LCK)', 'value': 'LCK'},
                                    ],
                                    value='All',
                                    placeholder='All'
                                )
                            ], style=dict(width='50%')
                        ),
                        html.Div(
                            [
                                html.Label('Statistic'),
                                dcc.Dropdown(
                                    id='stat-dropdown',
                                    options=[
                                        {'label': 'Win Rate', 'value': 'Win_Pct'},
                                        {'label': 'Average Gold per Minute', 'value': 'Avg_Gold_per_Minute'},
                                        {'label': 'Kills per Game', 'value': 'Kills_per_Game'},
                                        {'label': 'Objectives per Game', 'value': 'Objectives_per_Game'},
                                    ],
                                    value='Win_Pct',
                                    placeholder='Win Rate'
                                )
                            ], style=dict(width='50%')
                        ),
                    ],
                    className='row', style=dict(display='flex')
                ),
            dcc.Graph(id='top-team-stats'),
            html.Br(),
            html.H2('Kills vs. Objectives Scatter'),
            dcc.Graph(id='bubble-scatter'),
            dcc.RangeSlider(0, 1, 0.05, value=[0, 1], id='win-rate-slider'),
            html.H5('Win Rate Slider', style={'textAlign': 'center'})
        ]),
        dcc.Tab(label='Data', children=[
            html.H2('Teams Standings'),
            generate_table(teams_df[['Team', 'Tournament', 'Wins', 'Losses', 'Win_Pct']].sort_values(by='Win_Pct', ascending=False)),
            html.Br(),
            html.H2('Champions'),
            generate_table(display_champions_df[['Champion', 'Ovr_PickBan_Pct', 'Total_Played', 'Total_Banned', 'Total_Won']]),
            html.Br(),
            html.H2('Recent Games Results'),
            generate_table(display_games_df[['Date', 'Tournament', 'Patch', 'Blue', 'Red', 'Winner', 'Game_Length', 'Blue_Bans', 'Red_Bans', 'Blue_Picks', 'Red_Picks']], 25)
        ]),
    ]),
])

@app.callback(
    Output('champion-pb-rate', 'figure'),
    Input('region-dropdown-tab-1', 'value')
)

def build_champion_pb_bar(region):
    if region == 'All':
        top10_champions_df = champions_df.nlargest(10, 'Ovr_PickBan_Pct')
        champion_pb_bar = px.bar(top10_champions_df, x = 'Champion', y = 'Ovr_PickBan_Pct', text_auto=True)
    else:
        filter_column = region + '_PickBan_Pct'
        top10_champions_df = champions_df.nlargest(10, filter_column)
        champion_pb_bar = px.bar(top10_champions_df, x = 'Champion', y = filter_column, text_auto=True)
    champion_pb_bar.update_traces(marker_color = ['lightslategray']*10)
    return champion_pb_bar

@app.callback(
    Output('winner-side-pct', 'figure'),
    Input('region-dropdown-tab-1', 'value')
)

def build_winner_side_pie(region):
    if region == 'All':
        winner_side_pie = px.pie(games_df, names='Winner_Side', color='Winner_Side', color_discrete_map={'Blue': 'blue', 'Red': 'red'})
        winner_side_pie.update_layout(title = 'Percentage of Games Won on Red and Blue Side Across All Regions')
    else:
        winner_side_pie = px.pie(games_df[games_df.Tournament == region], names='Winner_Side', color='Winner_Side', color_discrete_map={'Blue': 'blue', 'Red': 'red'})
        winner_side_pie.update_layout(title = 'Percentage of Games Won on Red and Blue Side in ' + region)
    return winner_side_pie

@app.callback(
    Output('top-team-stats', 'figure'),
    Input('region-dropdown-tab-2', 'value'),
    Input('stat-dropdown', 'value')
)

def build_top_team_stat_bar(region, stat):
    if region == 'All':
        df = teams_df
    else:
        df = teams_df[teams_df.Tournament == region]
    df = df.nlargest(5, stat)
    if stat == 'Objectives_per_Game':
        top_team_stat_bar = px.bar(df, x = 'Team', y = ['Towers_per_Game', 'Drakes_per_Game', 'Barons_per_Game'])
        top_team_stat_bar.update_traces(hovertemplate = '%{y:.2f}')
        top_team_stat_bar.update_layout(legend_title_text = 'Objectives', yaxis_title = 'Objectives per Game', legend = {'traceorder': 'reversed'}, hovermode='x unified')
        # delete line above and include line below if/when lpl rift heralds are shown
        #top_team_stat_bar = px.bar(df, x = 'Team', y = ['Towers_per_Game', 'Drakes_per_Game', 'Heralds_per_Game', 'Barons_per_Game'], text_auto=True)
    else:
        top_team_stat_bar = px.bar(df, x = 'Team', y = stat, text_auto=True, labels = {'Win_Pct': 'Win Percentage', 'Avg_Gold_per_Minute': 'Average Gold per Minute', 'Kills_per_Game': 'Kills per Game'})
        top_team_stat_bar.update_traces(marker_color=['lightslategrey']*5)
    return top_team_stat_bar

@app.callback(
    Output('bubble-scatter', 'figure'),
    Input('win-rate-slider', 'value')
)

def build_bubble_scatter(win_rate_range):
    df = teams_df[(teams_df.Win_Pct >= win_rate_range[0]) & (teams_df.Win_Pct <= win_rate_range[1])]
    kills_vs_objectives_scatter = px.scatter(df, x = 'Kills_per_Game', y = 'Objectives_per_Game', color = 'Tournament', size = 'Win_Pct', hover_name = 'Team', size_max=33, 
    labels = {'Tournament': 'Region', 'Kills_per_Game': 'Kills per Game', 'Objectives_per_Game': 'Objectives Taken per Game', 'Win_Pct': 'Win Percentage'})
    kills_vs_objectives_scatter.update_layout(title_text='Kills vs. Objectives for All Teams', xaxis_title_text='Kills per Game', yaxis_title_text='Objectives Taken per Game')
    return kills_vs_objectives_scatter

if __name__ == '__main__':
    app.run_server(debug=True)
