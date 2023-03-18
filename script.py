import click
from get_dict_stats import all_team_stats, output_csv, output_json, output_sqlite, output_stdout
from main import team_name
from players_parametrs import players_param

'''
Hello!!!
This application uses commands like:
=============================================================================
python script.py grouped-teams
 - To divide teams by region. 
=============================================================================
python script.py players-stats --name Michael
"Must answer with the tallest and shortest player of that name or surname. 
 But there is almost no such data in the API, 
 so the command is not very useful"
=============================================================================
python script.py teams-stats --season 2017 --output stdout
"Command for summing up the statistics of teams for a certain season. 
 You can use other formats instead of strout to save, like json, csv, sqlite3"
=============================================================================
'''
class TeamGroup:

    def __init__(self, user_request, name=None, season=None, output=None):
        self.user_request = user_request
        self.name = name
        self.season = season
        self.output = output

    def run(self):
        if self.user_request == "grouped-teams":
            team_name()
        elif self.user_request == "players-stats":
            players_param(self.name)
        elif self.user_request == "teams-stats":
            dict_stats = all_team_stats(self.season)
            if self.output == 'csv':
                output_csv(dict_stats)
            elif self.output == 'json':
                output_json(dict_stats)
            elif self.output == 'sqlite':
                output_sqlite(dict_stats)
            elif self.output == 'stdout':
                output_stdout(dict_stats)
            else:
                click.echo(click.style('Wrong format written for saving!', fg='red', bold=True))
        else:
            print("No such command.\nWrite --help")

@click.command()
@click.argument('user-request', type=str)
@click.option("--name", "-n", type=str,
              help='Enter the player\'s name(DOES NOT WORK).')
@click.option("--season", "-s", type=int,
              help='Enter the season year. And then the --output command')
@click.option("--output", "-o", type=str,
              help='Specify the format: sqlite, json, csv, stdout. Example: python3 '
                   'script.py teams-stats --season 2017 --output stdout')
def cli(user_request, name, season, output):
    team_group = TeamGroup(user_request, name, season, output)
    team_group.run()


if __name__ == '__main__':
    cli()