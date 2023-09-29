def handler(event=None,context=None):
    print(event["scrape"])
    print(event["weather"])
    return {"report":"go climb"}