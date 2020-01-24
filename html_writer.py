import json

with open("sessions.json") as f:
    results = json.load(f)

with open("results.html", "w") as f:
    for result in results:
        f.write(
            f"Day: {result}<br>"
            f"{result[0]}"


                )
