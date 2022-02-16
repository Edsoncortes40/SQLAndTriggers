#!/usr/bin/python3
import psycopg2
import json
import sys
from types import *

def runPsy(conn, curs, jsonFile):
    with open(jsonFile) as f:
        for line in f:

##          ...

        conn.commit()
