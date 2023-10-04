# import requests
import json
import winter_alerts.config as config
from pprint import pprint
from winter_alerts.mytypes.response import MBResponse
from winter_alerts.mytypes.location import Location
from winter_alerts.mytypes.report import Reports, Report, Outlook, RecentAscent
from winter_alerts.mytypes.history import History, Yesterday
from typing import get_type_hints



ascents: dict[str, list[RecentAscent]] = {
    "Ben Nevis 800m" : [
        {
            "route": "tower ridge",
            "grade": "V",
            "date": "14th September"
        }
    ]
}

with open('./14day.json') as f:
    MBdata: MBResponse = json.loads(f.read())
weather: dict[str, MBResponse] = {"Ben Nevis 800m": MBdata}

def good_outlook(outlook: dict) -> bool:
    over_night_freezing = all([True if t < 0.0 else False for t in outlook['temperature_min']])
    return over_night_freezing



yesterday: dict[str, Yesterday] = {}
outlooks: dict[str,Outlook] = {}
for location in config.locations:
    data = weather[location["name"]]
    yesterday[location["name"]] = {k:v[0] for k,v in data["trend_day"].items() if k in get_type_hints(Yesterday)}

    # take 7 day outlook
    outlook_data = {k:v[1:8] for k,v in data["trend_day"].items()}

    outlook: Outlook = {k:v for k,v in data["trend_day"].items() if k in get_type_hints(Outlook)}
    outlook["good"] = good_outlook(outlook_data)
    outlooks[location['name']] = outlook

# save yesterday to database
history: History = {"timestamp": list(weather.values())[0]["trend_day"]["time"][0]}
history['locations'] = yesterday
pprint(history)

# evaluate history
items = [
    {
        "locations": {
            "Ben Nevis 800m": {
                "t": "0.0",
                "h": 0.3
            }
        },
        "pk": "partition_0",
        "timestamp": 12340
    },
    {
        "locations": {
            "Ben Nevis 800m": {
                "t": "0.0",
                "h": 8
            }
        },
        "pk": "partition_0",
        "timestamp": 12345
    }
]



reports:Reports = {
    "locations": []
}
for location in config.locations:
    # if history good and outlook good
    if not outlooks[location['name']]["good"]:
        # compose history
        days = [ day['locations'][location['name']] for day in items ]
        hist = {}
        for day in days:
            for k,v in day.items():
                if k in hist.keys():
                    hist[k].append(v)
                else:
                    hist[k] = [v]

        # package report
        report: Report = {}
        report["name"] = location['name']
        report["outlook"] = outlooks[location['name']]
        report["history"] = hist
        report["recent_acents"] = ascents[location['name']]
        reports["locations"].append(report)
        
# pprint(reports)
