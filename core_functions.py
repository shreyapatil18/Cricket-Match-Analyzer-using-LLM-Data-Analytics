import json

def load_match(file_path):
    with open(file_path) as f:
        return json.load(f)

def extract_innings(data):
    innings = data['innings']
    innings_data = []

    for inning in innings:
        team = inning.get("team", "Unknown")

        runs = 0
        wickets = 0
        boundaries = 0

        over_runs = []
        cumulative_runs = []
        wicket_overs = []

        current_total = 0

        for over in inning['overs']:
            over_total = 0
            over_number = over['over']

            for ball in over['deliveries']:
                r = ball['runs']['total']
                runs += r
                over_total += r

                if r == 4:
                    boundaries += 1

                if 'wickets' in ball:
                    wickets += len(ball['wickets'])
                    wicket_overs.append(over_number)

            current_total += over_total
            cumulative_runs.append(current_total)

        innings_data.append({
            "team": team,
            "runs": runs,
            "wickets": wickets,
            "boundaries": boundaries,
            "run_progression": cumulative_runs,
            "wicket_overs": wicket_overs
        })

    return innings_data