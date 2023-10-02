# import requests
import json
from pprint import pprint
from mytypes.response import MBResponse
from mytypes.location import Location

# r = requests.get("https://google.com")
# print(r)
# print(f"status: {r.status_code}")
# print(r.text)

def good_outlook(outlook: dict) -> bool:
    over_night_freezing = all([True if t < 0.0 else False for t in outlook['temperature_min']])
    low_humidity = all([True if h < 90 else False for h in outlook['relativehumidity_mean']])

    


locations: list[Location] = [
    {"name":"Ben Nevis Summit","lat":56.80,"lon":-5.00,"asl":1340},
    ]

yesterday = {}
for location in locations:
    # do request
    with open('./14day.json') as f:
        data: MBResponse = json.loads(f.read())

    yesterday[location["name"]] = {k:v[0] for k,v in data["trend_day"].items()}

    outlook = {k:v[1:] for k,v in data["trend_day"].items()}
    good_outlook(outlook)


# pprint(yesterday)