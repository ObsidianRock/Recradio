import requests
import datetime



DATE = datetime.datetime.utcnow()
DATE_FORMATTED = DATE.strftime('%a-%d-%H-%M')

FORMAT = '.mp3'


stream_url = 'http://media-ice.musicradio.com/LBCLondonMP3' # put in a module so can include other broadcasts


r = requests.get(stream_url, stream=True)

with open(DATE_FORMATTED+FORMAT, 'wb') as f:
    try:
        for block in r.iter_content(1024):
            f.write(block)
    except KeyboardInterrupt:
        pass
