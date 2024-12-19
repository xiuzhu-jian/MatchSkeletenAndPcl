from datetime import datetime


def ms_timestamp_to_str(ms_timestamp):
    return datetime.fromtimestamp(ms_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')


if __name__ == '__main__':
    print(ms_timestamp_to_str(1721716499514))
