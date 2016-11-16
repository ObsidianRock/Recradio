import requests
import datetime
import argparse
import configparser
import os
import sys
from threading import Thread, Event


def check_number(time):

    try:
        time = int(time)
    except ValueError:
        raise argparse.ArgumentTypeError('The time must a positive number')

    if time < 1:
        raise argparse.ArgumentTypeError('The time must be large then 1')
    else:
        return time


def config_file():
    config = configparser.ConfigParser()
    try:
        config.read_file(open('setting.ini'))
    except FileNotFoundError:
        print('configuration file does not exist')
        sys.exit()
    return dict(config.items())

def filename():
    DATE = datetime.datetime.utcnow()
    DATE_FORMATTED = DATE.strftime('%a-%d-%H-%M')

    FORMAT = '.mp3'

    return DATE_FORMATTED + FORMAT

def get_station(call):

    setting = config_file()
    try:
        station = setting['STATIONS'][call]
    except KeyError:
        print('Station does not exist')
        sys.exit()
    return station


def record(stop_event,file_name, station):

    r = requests.get(station, stream=True)

    with open(file_name, 'wb') as f:
        for block in r.iter_content(1024):
            f.write(block)
            if stop_event.is_set():
                break
    f.close()
    sys.exit()

def setup(call,time):
    file_name = filename()
    station = get_station(call)

    stop_event = Event()

    thr = Thread(target=record, args=(stop_event,file_name, station))
    thr.start()

    thr.join(time*60)

    if thr.is_alive():
        stop_event.set()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('station', type=str, help='Radio station')
    parser.add_argument('time', type=check_number, help='Time of recording')
    args = parser.parse_args()
    setup(args.station, args.time)


if __name__ == "__main__":
    main()
