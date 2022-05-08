import click
import requests


def team_name():
    basket = requests.get("https://www.balldontlie.io/api/v1/teams").json()
    list_commands = basket.get('data')
    region_list = {'Southeast': [], 'Southwest': [], 'Atlantic': [], 'Central': [], 'Northwest': [], 'Pacific': []}

    for list_command in list_commands:
        if list_command.get('division') == 'Southeast':
            region_list.get('Southeast').append(
                (list_command.get('full_name')) + ' (' + (list_command.get('abbreviation')) + ')')
        elif list_command.get('division') == 'Atlantic':
            region_list.get('Atlantic').append(
                (list_command.get('full_name')) + ' (' + (list_command.get('abbreviation')) + ')')
        elif list_command.get('division') == 'Central':
            region_list.get('Central').append(
                (list_command.get('full_name')) + ' (' + (list_command.get('abbreviation')) + ')')
        elif list_command.get('division') == 'Northwest':
            region_list.get('Northwest').append(
                (list_command.get('full_name')) + ' (' + (list_command.get('abbreviation')) + ')')
        elif list_command.get('division') == 'Pacific':
            region_list.get('Pacific').append(
                (list_command.get('full_name')) + ' (' + (list_command.get('abbreviation')) + ')')
        elif list_command.get('division') == 'Southwest':
            region_list.get('Southwest').append(
                (list_command.get('full_name')) + ' (' + (list_command.get('abbreviation')) + ')')
        else:
            print('Error from API')

    for region in region_list:
        click.echo(click.style(region, fg='green'))
        for team in region_list.get(region):
            print(f'    {team}')
