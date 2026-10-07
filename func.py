from espn_sports_api import NFL, NHL, Racing, MLB
import requests
from datetime import datetime
import re

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
            'awayTeamID': away['team']['id'],
            'homeTeamHEX': home['team']['color'],
            'homeTeamID': home['team']['color'],
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
            scorer = None
            shotType = None
            ytdScorerGoals = None
            assists = []
            for person in play['participants']:

                if person['type'] == 'scorer':
                    scorer = person['athlete']['displayName']
                    ytdScorerGoals = person['ytdGoals']
                    scorerIMG = person['athlete'].get('headshot', {}).get('href')
                    m = re.search(r"Goal \((\d+)\) (.+?)(?:,|$)", play['text'])
                    if m:
                        shotType = m.group(2)
                elif person['type'] == 'assister':
                    assists.append({
                        'assistName': person['athlete']['displayName'], 
                        'ytdAssists': person['ytdAssists'],
                        'assistIMG': person['athlete'].get('headshot', {}).get('href'),
                        })
            primaryAssist = assists[0] if len(assists) > 0 else None
            secondaryAssist = assists[1] if len(assists) > 1 else None
            
            goals.append({
                'teamID': play['team']['id'],
                'period': play['period']['number'],
                'strength': play['strength']['text'],
                'xCoord': play['coordinate'].get('x', {}),
                'yCoord': play['coordinate'].get('y', {}),
                'tog': play['clock']['displayValue'],
                'scorer': scorer,
                'scorerIMG': scorerIMG,
                'scorerYTDGoals': ytdScorerGoals,
                'shotType': shotType,
                'primaryAssist': primaryAssist if primaryAssist else None,
                'primaryAssistName': primaryAssist['assistName'] if primaryAssist else None,
                'primaryAssistYTD': primaryAssist['ytdAssists'] if primaryAssist else None,
                'primaryAssistIMG': primaryAssist['assistIMG'] if primaryAssist else None,
                'secondaryAssist': secondaryAssist if secondaryAssist else None,
                'secondaryAssistName': secondaryAssist['assistName'] if secondaryAssist else None,
                'secondaryAssistYTD': secondaryAssist['ytdAssists'] if secondaryAssist else None,
                'secondaryAssistIMG': secondaryAssist['assistIMG'] if secondaryAssist else None
            })

    return goals


def getImage(url):
    r = requests.get(url)
    return r.content

def periodName(n):
    if n <= 3:
        return ['1st', '2nd', '3rd'][n - 1]
    if n == 4:
        return "OT"
    return f"{n - 3}OT"



