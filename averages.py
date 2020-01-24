import json

with open("sessions.json") as f:
    reader = json.load(f)

for date in reader:
    for round in reader[date]['rounds']:
        for time in round:
            print(time['min'])
