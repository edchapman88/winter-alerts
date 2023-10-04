import winter_alerts.config as config
import boto3
from boto3.dynamodb.conditions import Key
from winter_alerts.mytypes.report import Reports, Report, Outlook, RecentAscent
from winter_alerts.mytypes.response import MBResponse
from winter_alerts.mytypes.history import History, Yesterday
from typing import get_type_hints

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('weatherHistory')

def good_outlook(outlook: dict) -> bool:
    over_night_freezing = all([True if t < 0.0 else False for t in outlook['temperature_min']])
    return over_night_freezing

def evaluate_history(query_items: list[History]):
    overnight_melt = set()
    for day in query_items:
        for name,conditions in day['locations'].items():
            print({'conditions':conditions})
            print({'min_temp':conditions['temperature_min']})
            if float(conditions['temperature_min']) > 0.0:
                overnight_melt.add(name)
    print({'overnight_melt':overnight_melt})
    return overnight_melt

def handler(event=None,context=None):
    ascents: dict[str, list[RecentAscent]] = event["scrape"]
    weather: dict[str, MBResponse] = event["weather"]

    yesterday: dict[str, Yesterday] = {}
    outlooks: dict[str, Outlook] = {}
    for location in config.locations:
        data = weather[location["name"]]

        yesterday[location["name"]] = {k:v[0] for k,v in data["trend_day"].items()}

        # take 7 day outlook
        outlook_data = {k:v[1:8] for k,v in data["trend_day"].items()}

        outlook: Outlook = {k:v for k,v in data["trend_day"].items() if k in get_type_hints(Outlook)}
        outlook["good"] = good_outlook(outlook_data)
        outlooks[location['name']] = outlook

    # save yesterday to database
    now = list(weather.values())[0]["trend_day"]["time"][0]
    history: History = {"pk":"partition_0", "timestamp": now}
    history['locations'] = {k:{k_:str(v_) for k_,v_ in v.items()} for k,v in yesterday.items()}
    table.put_item(
        Item=history
    )

    # evaluate history
    two_weeks = 1209600 # 2 weeks in seconds
    query = table.query(
        KeyConditionExpression=Key('pk').eq('partition_0') & Key('timestamp').gt(now - two_weeks)
    )
    overnight_melt = evaluate_history(query['Items'])
            
    reports:Reports = {
        "locations": []
    }
    for location in config.locations:
        # if history good and outlook good
        if outlooks[location['name']]["good"] and location['name'] not in overnight_melt:
            # compose history
            days = [ day['locations'][location['name']] for day in query['Items'] ]
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
            report["history"] = [ day[location['name']] for day in query['Items'] ]
            report["recent_acents"] = ascents[location['name']]
            reports["locations"].append(report)
        else:
            # for dev purposes_______
            # compose history
            days = [ day['locations'][location['name']] for day in query['Items'] ]
            hist = {}
            for day in days:
                for k,v in day.items():
                    if k in hist.keys():
                        hist[k].append(v)
                    else:
                        hist[k] = [v]
            report: Report = {}
            report["name"] = location['name']
            report["outlook"] = outlooks[location['name']]
            report["recent_acents"] = ascents[location['name']]
            reports['locations'].append("dev!")
            reports["locations"].append(report)
            # _______________________
    
    return {"report": reports}
