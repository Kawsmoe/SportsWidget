import json
import os
import time
import urllib.request
from func import nhlToday

CACHE = os.path.expanduser("~/.cache/waybar-nhl")
SHOW_SECONDS = 15
REFRESH_SECONDS = 300

os.makedirs(CACHE, exist_ok=True)


def logo_path(abbr, url):
    path = os.path.join(CACHE, f"{abbr}.png")
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return path


def point_at(name, target):
    link = os.path.join(CACHE, name)
    tmp = link + ".tmp"
    if os.path.lexists(tmp):
        os.remove(tmp)
    os.symlink(target, tmp)
    os.replace(tmp, link)


def show(game, tooltip):
    try:
        point_at("away.png", logo_path(game['awayAbbr'], game['awayLogo']))
        point_at("home.png", logo_path(game['homeAbbr'], game['homeLogo']))
    except Exception:
        pass
    time.sleep(1)  # let the image modules (1s poll) pick up the new logos first
    if game['state'] == 'pre':
        text = f"{game['awayAbbr']} @ {game['homeAbbr']}"
    else:
        text = f"{game['awayAbbr']} {game['awayScore']} - {game['homeScore']} {game['homeAbbr']}"
    status_file = os.path.join(CACHE, "status.json")
    with open(status_file + ".tmp", "w") as f:
        json.dump({"text": f"({game['status']})", "tooltip": tooltip}, f)
    os.replace(status_file + ".tmp", status_file)
    print(json.dumps({"text": text, "tooltip": tooltip}), flush=True)


games = []
last_fetch = 0
index = 0

while True:
    if time.time() - last_fetch > REFRESH_SECONDS:
        try:
            games = nhlToday()
        except Exception:
            pass
        last_fetch = time.time()

    if not games:
        print(json.dumps({"text": "No NHL games"}), flush=True)
        time.sleep(60)
        last_fetch = 0
        continue

    tooltip = "\n".join(
        f"{g['awayTeam']} {g['awayScore']} @ {g['homeTeam']} {g['homeScore']} ({g['status']})"
        for g in games
    )
    show(games[index % len(games)], tooltip)
    index += 1
    time.sleep(SHOW_SECONDS)
