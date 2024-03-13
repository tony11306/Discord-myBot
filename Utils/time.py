from datetime import datetime, timedelta, timezone

def get_current_time():
    '''
    Return Taiwan current time.
    '''
    return datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))

def get_24hours_ago():
    '''
    Return Taiwan time yesterday.
    '''
    return (get_current_time() + timedelta(hours=-24))