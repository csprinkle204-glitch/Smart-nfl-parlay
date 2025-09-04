from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# === CONFIG ===
RAPIDAPI_KEY = "383618465fmsh2808c026c9ed3dep16f274jsnb7222d486783"
RAPIDAPI_HOST = "nfl-api-data.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

# === SMART HELPERS ===

def get_current_week():
    today = datetime.today()
    start = datetime(today.year, 9, 1)
    delta_weeks = ((today - start).days // 7) + 1
    return min(max(delta_weeks, 1), 18)

def get_matchup_info(team1, team2):
    return {
        "home": team1,
        "away": team2,
        "location": "home"  # simple placeholder
    }

def fetch_player_stats(team):
    # Placeholder stub
    return {"key_players": ["QB1", "WR1", "RB1"]}

def fetch_odds_data(team1, team2):
    return {
        "spread": f"{team1} -3.5",
        "total": "48.5"
    }

def build_smart_parlay(team1, team2, leg_count):
    matchup = get_matchup_info(team1, team2)
    stats1 = fetch_player_stats(team1)
    stats2 = fetch_player_stats(team2)
    odds = fetch_odds_data(team1, team2)

    agents = ["PlayerPerformanceAgent", "TeamTrendsAgent", "OddsMovementAgent", "InjuryImpactAgent"]
    legs = []

    for i in range(min(leg_count, 10)):
        legs.append({
            "type": "player_prop",
            "description": f"{team1} key player over yards (leg {i+1})",
            "confidence": "high" if i < 3 else "medium",
            "sourceAgents": agents[:2] if i % 2 == 0 else agents[2:]
        })

    return {
        "legs": legs,
        "summary": f"{leg_count}-leg parlay using stats, trends, and odds from {team1} vs {team2} matchup"
    }

# === MAIN ENDPOINT ===

@app.route("/smart-parlay", methods=["GET"])
def smart_parlay():
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")
    leg_count = int(request.args.get("legs", 3))

    if not team1 or not team2:
        return jsonify({"error": "Missing team1 or team2"}), 400

    parlay = build_smart_parlay(team1, team2, leg_count)
    return jsonify(parlay)

# === HEALTH CHECK ===

@app.route("/", methods=["GET"])
def home():
    return "Smart NFL Parlay API is running!"

if __name__ == "__main__":
    app.run(debug=True)