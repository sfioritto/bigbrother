import json, os

# later you can detect what environment you are in, somehow, maybe
# a command line flag or something

path = os.path.dirname(__file__)
for key, value in json.loads(open(os.path.join(path, "dev.json")).read()).items():
    vars()[key] = value


