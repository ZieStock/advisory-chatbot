from datetime import datetime

def parseTime(time):
    if not time:
        return None
    try:
        return datetime.fromisoformat(time)
    except:
        return None