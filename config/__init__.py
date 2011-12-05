import json, os

# later you can detect what environment you are in, somehow, maybe
# a command line flag or something


for key, value in json.loads(open("config/dev.json").read()).items():
    vars()[key] = value


