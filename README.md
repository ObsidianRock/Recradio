# recradio

A Python command line application to download HTTP media streams.

## Packages Used

* Click (for creating beautiful command line interfaces)


## Getting Started

### Install Packages

```
pip install virtualenv
virtualenv venv
source venv/bin/activate (for windows venv\Scripts\activate)
pip install -r requirements.txt
```

## Setting

To add a stream, simply add the **name** and **url** in the setting.ini file.

format for setting.ini file:
[name] = [url]


## Running Application

### Help
```
python main.py --help
```

### Start stream

```
python main.py
```

then follow user input prompt

```
Enter Station: [from setting.ini file]
Number of minutes: [how long to record stream]
```

### forcefully Stop stream recording

```
CTRL + Esc (Windows)
Command-Shift-Option-Esc (Mac)
```
