from datetime import datetime, timedelta


def parse_date(timestamp):
    current_year = datetime.now().year

    try:
        return datetime.strptime(timestamp.strip(), '%b %d, %Y').date()
    except ValueError:
        pass

    try:
        return datetime.strptime(f"{timestamp.strip()}, {current_year}", '%b %d, %Y').date()
    except ValueError:
        pass

    try:
        if timestamp.endswith('h'):
            hours = int(timestamp[:-1])
            date = datetime.now() - timedelta(hours=hours)
            return date.date()
        elif timestamp.endswith('m'):
            minutes = int(timestamp[:-1])
            date = datetime.now() - timedelta(minutes=minutes)
            return date.date()
    except ValueError:
        pass

    return None
