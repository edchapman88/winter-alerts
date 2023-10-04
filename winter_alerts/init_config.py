import winter_alerts.config as config

def handler(event=None,context=None):
    return {"locations": config.locations}