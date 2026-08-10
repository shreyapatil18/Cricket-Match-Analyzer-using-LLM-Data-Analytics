import json
import os

def load_matches():
    matches = {}
    folder = "matches"

    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r") as f:
                matches[file] = json.load(f)

    return matches
