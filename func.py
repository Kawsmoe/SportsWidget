from espn_sports_api import NFL, NHL, Racing, MLB
import pandas as pd

nfl = NFL()
nhl = NHL()
mlb = MLB()
Racing = Racing("indycar")


def nflToday():
    today = nfl.today()
    return pd.json_normalize(today['events'])

def nhlToday():
    today = nhl.today()
    results = []



    for game in today['events']:
        comp = games['competitions'][i]
        teams = {c['homeAway']: c for c in comp['competitors']}
        home, away = teams["home"], teams['away']
        results.append({
            'homeTeam': home['team']['displayName'],
            'homeLogo': home['team']['logo'],
            'homeScore': home['score'],
            'homeRecord': home['records'][0],
            'awayTeam': away['team']['displayName'],
            'awayLogo': away['team']['logo'],
            'awayScore': away['score'],
            'awayRecord': away['records'][0],
        })


    return results
    
    

