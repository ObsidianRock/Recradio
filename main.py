import requests
import datetime
import argparse
import configparser
import os
import sys
from stations import STATIONS



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
    basedir = os.path.abspath(os.path.dirname(__file__))
    config = configparser.ConfigParser()
    try:
        config.read_file(open('setting.ini'))
    except FileNotFoundError:
        print('configuration file does not exist')
        sys.exit()
    return dict(config.item())

def filename():
    DATE = datetime.datetime.utcnow()
    DATE_FORMATTED = DATE.strftime('%a-%d-%H-%M')

    FORMAT = '.mp3'

    return DATE_FORMATTED + FORMAT


def record(call,time):

    station = STATIONS[call]

    r = requests.get(station, stream=True)

    with open(filename(), 'wb') as f:
        try:
            for block in r.iter_content(1024):
                f.write(block)
        except KeyboardInterrupt:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('station', type=str, help='Radio station')
    parser.add_argument('time', type=check_number, help='Time of recording')
    args = parser.parse_args()




if __name__ == "__main__":
    main()
