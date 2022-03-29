import click
from get_dict_stats import all_team_stats, output_csv, output_json, output_sqlite, output_stdout
from main import team_name


@click.command()
@click.argument('user-request', type=str)
@click.option("--name", "-n", help='Enter the player\'s name(DOES NOT WORK).')
@click.option("--season", "-s", type=int, help='Enter the season year. And then the --output command')
@click.option("--output", "-o", type=str, help= 'Specify the format: sqlite, json, csv, stdout.')
def team_group(user_request, name, season, output):
    if user_request == "grouped-teams":
        team_name()
    elif user_request == "players-stats":
        pass

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
        print("No such comand.\nWrite --help")


if __name__ == '__main__':
    team_group()
