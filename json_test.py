import json

with open('sessions.json') as f:
    sessions = json.load(f)

print(len(sessions))
