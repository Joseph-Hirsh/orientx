def parse_metric(num_str):
    if num_str is None:
        return None

    num_str = num_str.strip().upper()

    if num_str.endswith('K'):
        return int(float(num_str[:-1]) * 1_000)
    elif num_str.endswith('M'):
        return int(float(num_str[:-1]) * 1_000_000)
    elif num_str.endswith('B'):
        return int(float(num_str[:-1]) * 1_000_000_000)
    else:
        try:
            return int(num_str)
        except ValueError:
            return None


