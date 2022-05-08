import requests
import click

name = 'Beasley'


def players_param(name):
    click.clear()
    start_url_api = 'https://www.balldontlie.io/api/v1/players?per_page=100'
    page_max = requests.get(start_url_api).json()
    the_tallest_player = []
    the_heaviest_player = []
    players_list = []
    this_is_bad = 0
    this_is_bad2 = 0
    with click.progressbar(range((page_max.get('meta').get('total_pages'))), label='Check layers statistics') as bar:
        for page in bar:
            team_stats = requests.get(start_url_api + "&page=" + str(page)).json()
            for player in team_stats.get('data'):
                if player.get('first_name') != name or \
                        player.get('last_name') != name:
                    click.clear()
                    return print('\nThe tallest player: Not found\nThe heaviest player: Not found')
                else:
                    if player.get('height_feet') != None and player.get('weight_feet') != None:
                        the_tallest_player.append({'name': str(player.get('first_name') + player.get('last_name')),
                                                   'height': float(player['height_feet'] * 30.48 / 100 +
                                                                   player['height_inches'] * 2.54 / 100)})
                        the_heaviest_player.append({'name': str(player.get('first_name') + player.get('last_name')),
                                                    'weight': int(player['height_feet'] * 0.453592)})
                    else:
                        this_is_bad = 1

                    if player.get('weight_pounds') != None:
                        the_heaviest_player.append({'name': str(player.get('first_name') + player.get('last_name')),
                                                    'weight': int(player['weight_pounds'] * 0.453592)})
                    else:
                        this_is_bad2 = 1
    click.clear()
    if this_is_bad == 0:
        the_tallest_player = sorted(players_list, key=lambda d: d['height'])
        the_tallest_player.reverse()
        print('\nThe tallest player: ')
        for player in range(len(the_tallest_player)):
            if the_tallest_player[0].get('height') == the_tallest_player[player].get('height'):
                print(
                    the_tallest_player[player].get('name') + ' ' + the_tallest_player[player].get('height') + 'meters')
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
