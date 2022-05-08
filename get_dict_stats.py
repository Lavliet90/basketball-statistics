import requests
import csv
import json
import sqlite3
import click
import time


def all_team_stats(season):
    start_time = time.time()
    click.clear()
    teams_search = requests.get("https://www.balldontlie.io/api/v1/teams").json()

    list_teams = [((team.get('full_name')) + ' (' + (team.get('abbreviation')) + ')')
                  for team in teams_search.get('data')]
    stats_teams = [{"team_name": team,
                    'won_game_as_home_team': 0,
                    'won_game_as_visitor_team': 0,
                    'lost_game_as_home_team': 0,
                    'lost_game_as_visitor_team': 0} for team in list_teams]

    season_pages = "https://www.balldontlie.io/api/v1/games?seasons[]=" + str(season)
    page_max = requests.get(season_pages + '&per_page=100').json()
    with click.progressbar(range((page_max.get('meta').get('total_pages')) + 1), label='Check teams statistics') as bar:
        for page in bar:
            team_stats = requests.get(season_pages + '&page=' + str(page) + '&per_page=100').json()
            for team_stat in team_stats.get('data'):
                if team_stat.get('home_team_score') > team_stat.get('visitor_team_score'):
                    for team in stats_teams:
                        if (team_stat.get('home_team').get('full_name') + ' (' + team_stat.get('home_team')
                                .get('abbreviation') + ')') == team.get('team_name'):
                            team['won_game_as_home_team'] += 1
                        elif (team_stat.get('visitor_team').get('full_name') + ' (' +
                              team_stat.get('visitor_team').get('abbreviation') + ')') == team.get('team_name'):
                            team['lost_game_as_home_team'] += 1
                        else:
                            continue
                elif team_stat.get('home_team_score') < team_stat.get('visitor_team_score'):
                    for stat_team in stats_teams:
                        if (team_stat.get('home_team').get('full_name') + ' (' + team_stat.get('home_team')
                                .get('abbreviation') + ')') == stat_team.get('team_name'):
                            stat_team['lost_game_as_visitor_team'] += 1
                        elif (team_stat.get('visitor_team').get('full_name') + ' (' +
                              team_stat.get('visitor_team').get('abbreviation') + ')') == stat_team.get('team_name'):
                            stat_team['won_game_as_visitor_team'] += 1

        click.clear()
    click.echo(click.style('We have collected data!', fg='green'))
    print(time.time() - start_time)
    return stats_teams


def output_csv(dict_stasts):
    team_names = [team_name.get('team_name') for team_name in dict_stasts]
    won_game_as_home_team = [team_name.get('won_game_as_home_team') for team_name in dict_stasts]
    won_game_as_visitor_team = [team_name.get('won_game_as_visitor_team') for team_name in dict_stasts]
    lost_game_as_home_team = [team_name.get('lost_game_as_home_team') for team_name in dict_stasts]
    lost_game_as_visitor_team = [team_name.get('lost_game_as_visitor_team') for team_name in dict_stasts]

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
            'INSERT INTO user(team_name, won_game_as_home_team, won_game_as_visitor_team, lost_game_as_home_team, '
            'lost_game_as_visitor_team)'
            'VALUES(?,?,?,?,?);', team_stat)
    conn.commit()


def output_stdout(dict_stasts):
    for team_stats in dict_stasts:
        print(team_stats.get('team_name'))
        print('     won game as home team: ' + str(team_stats.get('won_game_as_home_team')))
        print('     won game as visitor team: ' + str(team_stats.get('won_game_as_visitor_team')))
        print('     lost game as home team: ' + str(team_stats.get('lost_game_as_home_team')))
        print('     lost game as visitor team: ' + str(team_stats.get('lost_game_as_visitor_team')))
