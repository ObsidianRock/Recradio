import requests
import datetime

from stations import *



def filename():


    DATE = datetime.datetime.utcnow()
    DATE_FORMATTED = DATE.strftime('%a-%d-%H-%M')

    FORMAT = '.mp3'

    return DATE_FORMATTED + FORMAT


def record(station):

    r = requests.get(station, stream=True)

    with open(filename(), 'wb') as f:
        try:
            for block in r.iter_content(1024):
                f.write(block)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    record()
