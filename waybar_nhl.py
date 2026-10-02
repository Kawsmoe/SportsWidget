import json
from func import nhlToday

games = nhlToday()
text = " | ".join(f"{g['awayTeam'][:3].upper()} {g['awayScore']}-{g['homeScore']} {g['homeTeam'][:3].upper()}" for g in games[:2])
tooltip = "\n".join(f"{g['awayTeam']} {g['awayScore']} @ {g['homeTeam']} {g['homeScore']}" for g in games)
print(json.dumps({"text": f"🏒 {text}", "tooltip": tooltip}))
