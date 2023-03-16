import click
import requests


def team_name():
    basket = requests.get("https://www.balldontlie.io/api/v1/teams").json()
    list_commands = basket.get('data')
    region_list = {
        'Southeast': [],
        'Southwest': [],
        'Atlantic': [],
        'Central': [],
        'Northwest': [],
        'Pacific': []
    }

    for list_command in list_commands:
        name_team_and_tag = '{} ({})'.format(
            list_command.get('full_name'),
            list_command.get('abbreviation')
        )
        devision_team = list_command.get('division')
        region_list.get(
            devision_team, "Error from API"
        ).append(name_team_and_tag)

    for region in region_list:
        click.echo(click.style(region, fg='green'))
        for team in region_list.get(region):
            print(f'    {team}')