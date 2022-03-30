import requests
import click

name = 'Beasley'

error = 'Not found'
#
# def players_param(name):

def players_param(name):
    click.clear()
    page_max = requests.get("https://www.balldontlie.io/api/v1/players?per_page=100").json()
    the_tallest_player = []
    the_heaviest_player = []
    players_list = []
    this_is_bad = 0
    this_is_bad2 = 0
    with click.progressbar(range((page_max.get('meta').get('total_pages'))), label='Check layers statistics') as bar:
        for page in bar:
            team_stats = requests.get("https://www.balldontlie.io/api/v1/players?per_page=100&page=" + str(page)).json()
            for player in range(100):
                if team_stats.get('data')[player].get('first_name') != name or \
                        team_stats.get('data')[player].get('last_name') != name:
                    click.clear()
                    return print('\nThe tallest player: Not found\nThe heaviest player: Not found')
                else:
                    if team_stats.get('data')[player].get('height_feet') != None and \
                            team_stats.get('data')[player].get('weight_feet') != None:
                        the_tallest_player.append({'name': str(team_stats.get('data')[player].get('first_name') +
                                                               team_stats.get('data')[player].get('last_name')),
                                                   'height': float(
                                                       team_stats.get('data')[player]['height_feet'] * 30.48 / 100 +
                                                       team_stats.get('data')[player]['height_inches'] * 2.54 / 100)})
                        the_heaviest_player.append({'name': str(team_stats.get('data')[player].get('first_name') +
                                                                team_stats.get('data')[player].get('last_name')),
                                                    'weight': int(team_stats.get('data')[player]['height_feet'] * 0,
                                                                  453592)})
                    else:
                        this_is_bad = 1

                    if team_stats.get('data')[player].get('weight_pounds') != None:
                        the_heaviest_player.append({'name': str(team_stats.get('data')[player].get('first_name') +
                                                                team_stats.get('data')[player].get('last_name')),
                                                    'weight': int(team_stats.get('data')[player]['weight_pounds'] * 0,
                                                                  453592)})
                    else:
                        this_is_bad2 = 1
    click.clear()
    if this_is_bad == 0:
        the_tallest_player = sorted(players_list, key=lambda d: d['height'])
        the_tallest_player.reverse()
        print('\nThe tallest player: ')
        for player in range(len(the_tallest_player)):
            if the_tallest_player[0].get('height') == the_tallest_player[player].get('height'):
                print(the_tallest_player[player].get('name') + ' ' + the_tallest_player[player].get('height') + 'meters')
    else:
        print('\nThe tallest player: Not found')

    if this_is_bad2 == 0:
        the_heaviest_player = sorted(players_list, key=lambda d: d['weight'])
        the_heaviest_player.reverse()
        print('\nThe heaviest player: ')
        for player in range(len(the_heaviest_player)):
            if the_heaviest_player[0].get('weight') == the_heaviest_player[player].get('weight'):
                print(the_heaviest_player[player].get('weight') + ' ' + the_heaviest_player[player].get(
                    'weight') + 'kilograms')
    else:
        print('\nThe heaviest player: Not found')