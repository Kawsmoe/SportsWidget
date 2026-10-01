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
    events = today['events']
    


