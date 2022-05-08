import click
from get_dict_stats import all_team_stats, output_csv, output_json, output_sqlite, output_stdout
from main import team_name
from players_parametrs import players_param

'''
Hello!!!
This application uses commands like:
"python3 script.py grouped-teams" - To divide teams by region. 
"python3 script.py players-stats --name Michael" - Must answer with the tallest and shortest player of that name or 
                                                    surname. But there is almost no such data in the API, 
                                                    so the command is not very useful  
"python3 script.py teams-stats --season 2017 --output stdout" - Command for summing up the statistics of teams for a 
                                                                certain season. You can use other formats instead of 
                                                                strout to save, like json, csv, sqlite3
'''


@click.command()
@click.argument('user-request', type=str)
@click.option("--name", "-n", type=str, help='Enter the player\'s name(DOES NOT WORK). ')
@click.option("--season", "-s", type=int, help='Enter the season year. And then the --output command')
@click.option("--output", "-o", type=str, help='Specify the format: sqlite, json, csv, stdout. Example: python3 '
                                               'script.py teams-stats --season 2017 --output stdout')
def team_group(user_request, name, season, output):
    if user_request == "grouped-teams":
        team_name()
    elif user_request == "players-stats":
        players_param(name)
    elif user_request == "teams-stats":
        dict_stasts = all_team_stats(season)
        if output == 'csv':
            output_csv(dict_stasts)
        elif output == 'json':
            output_json(dict_stasts)
        elif output == 'sqlite':
            output_sqlite(dict_stasts)
        elif output == 'stdout':
            output_stdout(dict_stasts)
        else:
            click.echo(click.style('Wrong format written for saving!', fg='red', bold=True))
    else:
        print("No such command.\nWrite --help")


if __name__ == '__main__':
    team_group()
