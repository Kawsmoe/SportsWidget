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
            'time': formatTime(game['date'])
        })


    return results


def nhlYesterday():
    today = nhl.yesterday()
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
        })


    return results


def getTeamImage(url):
    r = requests.get(url)
    return r.content



