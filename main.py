import configparser
import datetime
import sys

from threading import Thread, Event

import click
import keyboard
import requests


def config_file():
    config = configparser.ConfigParser()
    try:
        config.read_file(open('setting.ini'))
    except FileNotFoundError:
        print('configuration file does not exist')
        sys.exit()
    return dict(config.items())


def filename():
    date_now = datetime.datetime.utcnow()
    date_formatted = date_now.strftime('%a-%d-%H-%M')
    file_format = '.mp3'
    return date_formatted + file_format


def get_station(call):

    setting = config_file()
    try:
        station = setting['STATIONS'][call]
    except KeyError:
        print('Station does not exist')
        sys.exit()
    return station


def record(stop_event, file_name, station):

    r = requests.get(station, stream=True)

    with open(file_name, 'wb') as f:
        for block in r.iter_content(1024):
            f.write(block)
            if keyboard.is_pressed('esc') or stop_event.is_set():
                break
    f.close()
    sys.exit()


@click.command()
@click.option('--station',
              prompt='Enter Station',
              help='Station to record')
@click.option('--time',
              prompt='Number of minutes',
              type=click.INT,
              help='Number of minutes to record')
def setup(station, time):
    click.clear()
    if int(time) < 1:
        click.secho('Time must be greater than 0', fg='red')
        sys.exit()

    file_name = filename()
    station_name = get_station(station)

    stop_event = Event()
    thr = Thread(target=record, args=(stop_event, file_name, station_name), daemon=True)
    thr.start()
    thr.join(int(time)*60)

    if thr.is_alive():
        stop_event.set()


if __name__ == "__main__":
    setup()
