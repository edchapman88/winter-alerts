import requests
import os
import winter_alerts.config as config
from winter_alerts.mytypes.response import MBResponse

def handler(event=None,context=None):
    data: dict[str, MBResponse] = {}
    base_url = f"https://my.meteoblue.com/packages/trend-day?apikey={os.environ['MB_KEY']}&history_days=1&winddirection=2char&windspeed=mph&timeformat=timestamp_utc"
    for location in config.locations:
        url = base_url + f"&lat={location['lat']}&lon={location['lon']}&asl={location['asl']}&name={location['name']}"
        r = requests.get(url)
        data[location["name"]] = r.json()

    return {"weather": data, "scrape": event["scrape"]}