# Traphite

## Requirements

* Python2 or Python3
* PIP

## Ubuntu sample installation:

```
apt-get install pip
pip install -r requirements.txt 
```

## Starting

Command line parameters:
```
usage: main.py [-h] --host HOST [--port PORT] [--interface INTERFACE]

Traphite - Network bandwidth logging for Graphite

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           StatsD Hostname
  --port PORT           StatsD Port
  --interface INTERFACE Network interface for monitoring
```