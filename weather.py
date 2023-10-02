import requests
def handler(event=None,context=None):
    r = requests.get("https://google.com")
    print(r)
    print(f"status: {r.status_code}")
    print(r.json())

    data = [{"weather": "good"}]
    # return {"weather": data, "scrape": event["scrape"]}