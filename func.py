from espn_sports_api import NFL, NHL, Racing, MLB
import requests
from datetime import datetime

nfl = NFL()
nhl = NHL()
mlb = MLB()
Racing = Racing("indycar")

def formatTime(iso):
    dt = datetime.fromisoformat(iso).astimezone()
    return dt.strftime("%-I:%M %p")

def nhlToday():
    today = nhl.today()
    results = []

    for game in today['events']:
        comp = game['competitions'][0]
        teams = {c['homeAway']: c for c in comp['competitors']}
        home, away = teams["home"], teams['away']
        results.append({
            'status': comp['status']['type']['shortDetail'],
            'state': comp['status']['type']['state'],
            'homeTeam': home['team']['displayName'],
            'homeAbbr': home['team']['abbreviation'],
            'homeLogo': home['team']['logo'],
            'homeScore': home['score'],
            'homeRecord': home['records'][0]['summary'],
            'awayTeam': away['team']['displayName'],
            'awayAbbr': away['team']['abbreviation'],
            'awayLogo': away['team']['logo'],
            'awayScore': away['score'],
            'awayRecord': away['records'][0]['summary'],
            'time': formatTime(game['date']),
            'awayTeamHEX': away['team']['color'],
            'homeTeamHEX': home['team']['color'],
            'homeProbGoalie': home['probables'][0]['athlete']['fullName'],
            'awayProbGoalie': away['probables'][0]['athlete']['fullName'],
            'gameID': game['id'],
            'awayLocation': away['team']['location'],
            'awayName': away['team']['name'],
            'homeLocation': home['team']['location'],
            'homeName': home['team']['name'],
            'awayPeriods': [l['displayValue'] for l in away.get('linescores', [])],
            'homePeriods': [l['displayValue'] for l in home.get('linescores', [])],
        })


    return results


def getGoals(gameID):
    nhlpbp = nhl.playbyplay(gameID)

    goals = []

    for play in nhlpbp['plays']:
        if play['scoringPlay']:
            goals.append({
                'teamID': play['team']['id'],
                'period': play['period']['number'],
                'strength': play['strength']['text'],
                'xCoord': play['coordinate']['x'],
                'yCoord': play['coordinate']['y'],
                'tog': play['clock']['displayValue'],
                'scorer': play['participants'][0]['athlete']['displayName'],
                'primaryAssist': play['participants'][1]['athlete']['displayName'],
                'secondaryAssist': play['participants'][2]['athlete']['displayName'],


            })


def getImage(url):
    r = requests.get(url)
    return r.content

def periodName(n):
    if n <= 3:
        return ['1st', '2nd', '3rd'][n - 1]
    if n == 4:
        return "OT"
    return f"{n - 3}OT"



