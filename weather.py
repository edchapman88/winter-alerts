def handler(event=None,context=None):
    data = [{"weather": "good"}]
    return {"weather": data, "scrape": event["scrape"]}