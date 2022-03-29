import requests

def team_name():
    basket = requests.get("https://www.balldontlie.io/api/v1/teams").json()
    southeast_teams = []
    southwest_teams = []
    atlantic_teams = []
    central_teams = []
    northwest_teams = []
    pacific_teams = []

    for i in range(len(basket.get('data'))):
        if basket.get('data')[i].get('division') == 'Southeast':
            southeast_teams.append(
                (basket.get('data')[i].get('full_name')) + ' (' + (basket.get('data')[i].get('abbreviation')) + ')')
        elif basket.get('data')[i].get('division') == 'Atlantic':
            atlantic_teams.append(
                (basket.get('data')[i].get('full_name')) + ' (' + (basket.get('data')[i].get('abbreviation')) + ')')
        elif basket.get('data')[i].get('division') == 'Central':
            central_teams.append(
                (basket.get('data')[i].get('full_name')) + ' (' + (basket.get('data')[i].get('abbreviation')) + ')')
        elif basket.get('data')[i].get('division') == 'Northwest':
            northwest_teams.append(
                (basket.get('data')[i].get('full_name')) + ' (' + (basket.get('data')[i].get('abbreviation')) + ')')
        elif basket.get('data')[i].get('division') == 'Pacific':
            pacific_teams.append(
                (basket.get('data')[i].get('full_name')) + ' (' + (basket.get('data')[i].get('abbreviation')) + ')')
        elif basket.get('data')[i].get('division') == 'Southwest':
            southwest_teams.append(
                (basket.get('data')[i].get('full_name')) + ' (' + (basket.get('data')[i].get('abbreviation')) + ')')
        else:
            print('Error from API')

    print('Southeast')
    for team in southeast_teams:
        print(f'    {team}')
    print('Southwest')
    for team in southwest_teams:
        print(f'    {team}')
    print('Atlantic')
    for team in atlantic_teams:
        print(f'    {team}')
    print('Central')
    for team in central_teams:
        print(f'    {team}')
    print('Nortwest')
    for team in northwest_teams:
        print(f'    {team}')
    print('Pacific')
    for team in pacific_teams:
        print(f'    {team}')
