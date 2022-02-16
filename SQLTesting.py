import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse
import pickle

from psy import *
from orm import *

correct_answers = []

def pout(ans):
    print("--------- Your Query Answer ---------")
    for t in ans:
        print(t)
    print("")

def executePrint(s):
        cur.execute(s)
        ans = cur.fetchall()
        print(ans)
        return ans

def runQueries():
    cur.execute("SELECT * FROM customers WHERE customerid='cust1000'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    cur.execute("SELECT * FROM customers WHERE customerid = 'cust1001'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

    cur.execute("SELECT flightid, customerid, flightdate FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
    ans = cur.fetchall()
    correct_answers.append(ans)
    pout(ans)

def delQueries():
    cur.execute("DELETE FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
    cur.execute("DELETE FROM customers WHERE (customerid='cust1000')")
    cur.execute("DELETE FROM customers WHERE (customerid='cust1001')")
    conn.commit()


correct_answers = []

conn = psycopg2.connect("dbname=flightsskewed user=vagrant password=vagrant")
#conn = psycopg2.connect("dbname=flightsskewed user=keleher")
cur = conn.cursor()

try:
    delQueries()

    print("========== Executing PSY")
    runPsy(conn, cur, "example.json")
    cur.execute("DELETE FROM numberofflightstaken;")
    conn.commit()
    runQueries()

    delQueries()

    print("========== Executing ORM")
    runORM("example.json")
    runQueries()
	
    cur.execute("SELECT COUNT(*) FROM numberofflightstaken;")
    ans = cur.fetchall()
    pout(ans)

except:
    print(sys.exc_info())
    raise

            

with open("correct_answers.pickle", "wb") as f:
    pickle.dump(correct_answers, f)

print("wrote {} answers".format(len(correct_answers)))
