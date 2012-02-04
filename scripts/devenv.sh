#!/bin/bash

cd ~
git clone git@github.com:sfioritto/BigBrother bigbrother
cd bigbrother/
virtualenv env
. env/bin/activate
pip install web.py
pip install PIL
pip install sqlalchemy
pip install psycopg2
dropdb bigbrother
createdb bigbrother
python scripts/createdb.py 
python scripts/createdb.py 
