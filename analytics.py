import pandas as pd

# ---------------- MATCH SUMMARY ----------------
def get_summary(match):
    info = match["info"]

    team1, team2 = info["teams"]

    outcome = info["outcome"]
    winner = outcome.get("winner", "No Result")

    if "runs" in outcome.get("by", {}):
        margin = f"{outcome['by']['runs']} runs"
    elif "wickets" in outcome.get("by", {}):
        margin = f"{outcome['by']['wickets']} wickets"
    else:
        margin = "N/A"

    return team1, team2, winner, margin


# ---------------- INNINGS DATAFRAME ----------------
def innings_dataframe(match):
    rows = []

    innings_list = match["innings"]

    for i, innings in enumerate(innings_list):
        team = innings["team"]

        total_runs = 0
        wickets = 0

        for over_data in innings["overs"]:
            over = over_data["over"]

            for ball in over_data["deliveries"]:
                runs = ball["runs"]["total"]
                total_runs += runs

                if "wickets" in ball:
                    wickets += 1

                rows.append({
                    "innings": i + 1,
                    "team": team,
                    "over": over,
                    "runs": runs,
                    "cumulative_runs": total_runs,
                    "wickets": wickets
                })

    df = pd.DataFrame(rows)
    return df
