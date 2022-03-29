import requests
import csv
import json
import sqlite3


def all_team_stats(season):
    list_teams = []
    stats_teams = []
    print('wait a minute...')
    teams_search = requests.get("https://www.balldontlie.io/api/v1/teams").json()
    for i in range(len(teams_search.get('data'))):
        list_teams.append((teams_search.get('data')[i].get('full_name')) + ' (' + (
            teams_search.get('data')[i].get('abbreviation')) + ')')

    for team in list_teams:
        team_for_list = {
            "team_name": team,
            'won_game_as_home_team': 0,
            'won_game_as_visitor_team': 0,
            'lost_game_as_home_team': 0,
            'lost_game_as_visitor_team': 0
        }
        stats_teams.append(team_for_list)

    page_max = requests.get("https://www.balldontlie.io/api/v1/games?seasons[]=" + str(season) + '&per_page=100').json()
    for page in range((page_max.get('meta').get('total_pages')) + 1):

        team_stats = requests.get("https://www.balldontlie.io/api/v1/games?seasons[]=" + str(season) + '&page=' + str(
            page) + '&per_page=100').json()
        for j in range(len(team_stats.get('data'))):
            if team_stats.get('data')[j].get('home_team_score') > team_stats.get('data')[j].get('visitor_team_score'):
                for i in range(len(stats_teams)):
                    if (team_stats.get('data')[j].get('home_team').get('full_name') + ' (' + team_stats.get('data')[
                        j].get('home_team').get('abbreviation') + ')') == stats_teams[i].get('team_name'):
                        stats_teams[i]['won_game_as_home_team'] += 1
                    elif (team_stats.get('data')[j].get('visitor_team').get('full_name') + ' (' +
                          team_stats.get('data')[j].get('visitor_team').get('abbreviation') + ')') == stats_teams[
                        i].get('team_name'):
                        stats_teams[i]['lost_game_as_home_team'] += 1
                    else:
                        continue
            elif team_stats.get('data')[j].get('home_team_score') < team_stats.get('data')[j].get('visitor_team_score'):
                for i in range(len(stats_teams)):
                    if (team_stats.get('data')[j].get('home_team').get('full_name') + ' (' + team_stats.get('data')[
                        j].get('home_team').get('abbreviation') + ')') == stats_teams[i].get('team_name'):
                        stats_teams[i]['lost_game_as_visitor_team'] += 1
                    elif (team_stats.get('data')[j].get('visitor_team').get('full_name') + ' (' +
                          team_stats.get('data')[j].get('visitor_team').get('abbreviation') + ')') == stats_teams[
                        i].get('team_name'):
                        stats_teams[i]['won_game_as_visitor_team'] += 1
                    else:
                        continue
            else:
                continue
    print('ready')
    return stats_teams


def output_csv(dict_stasts):
    team_names = []
    for team_name in dict_stasts:
        team_names.append(team_name.get('team_name'))

    won_game_as_home_team = []
    for team_name in dict_stasts:
        won_game_as_home_team.append(team_name.get('won_game_as_home_team'))

    won_game_as_visitor_team = []
    for team_name in dict_stasts:
        won_game_as_visitor_team.append(team_name.get('won_game_as_visitor_team'))

    lost_game_as_home_team = []
    for team_name in dict_stasts:
        lost_game_as_home_team.append(team_name.get('lost_game_as_home_team'))

    lost_game_as_visitor_team = []
    for team_name in dict_stasts:
        lost_game_as_visitor_team.append(team_name.get('lost_game_as_visitor_team'))

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(team_names)
        writer.writerow(won_game_as_home_team)
        writer.writerow(won_game_as_visitor_team)
        writer.writerow(lost_game_as_home_team)
        writer.writerow(lost_game_as_visitor_team)


def output_json(dict_stasts):
    with open('output.json', 'w') as outfile:
        json.dump(dict_stasts, outfile)


def output_sqlite(dict_stasts):
    conn = sqlite3.connect('teams_stats.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS user(
    team_name TEXT,
    won_game_as_home_team INT,
    won_game_as_visitor_team INT,
    lost_game_as_home_team INT,
    lost_game_as_visitor_team INT);
    ''')
    conn.commit()

    for i in range(len(dict_stasts)):
        team_stat = (dict_stasts[i].get('team_name'), dict_stasts[i].get('won_game_as_home_team'),
                     dict_stasts[i].get('won_game_as_visitor_team'), dict_stasts[i].get('lost_game_as_home_team'),
                     dict_stasts[i].get('lost_game_as_visitor_team'))
        cur.execute(
            'INSERT INTO user(team_name, won_game_as_home_team, won_game_as_visitor_team, lost_game_as_home_team, lost_game_as_visitor_team)'
            'VALUES(?,?,?,?,?);', team_stat)
    conn.commit()

def output_stdout(dict_stasts):
    for i in range(len(dict_stasts)):
        print(dict_stasts[i].get('team_name'))
        print('     won game as home team: ' + str(dict_stasts[i].get('won_game_as_home_team')))
        print('     won game as visitor team: ' + str(dict_stasts[i].get('won_game_as_visitor_team')))
        print('     lost game as home team: ' + str(dict_stasts[i].get('lost_game_as_home_team')))
        print('     lost game as visitor team: ' + str(dict_stasts[i].get('lost_game_as_visitor_team')))