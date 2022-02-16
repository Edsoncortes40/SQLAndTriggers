#!/usr/bin/python3
import psycopg2
import json
import sys
from types import *
from psy import *

def pout(ans):
    print("--------- Your Query Answer ---------")
    for t in ans:
        print(t)
    print("")

#conn = psycopg2.connect("dbname=flightsskewed user=keleher")
conn = psycopg2.connect("dbname=flightsskewed user=vagrant password=vagrant")
cur = conn.cursor()

cur.execute("DELETE FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
cur.execute("DELETE FROM customers WHERE customerid='cust1000'")
cur.execute("DELETE FROM customers WHERE customerid='cust1001'")
conn.commit()

runPsy(conn, cur, "example.json")

cur.execute("SELECT * FROM customers WHERE customerid='cust1000'")
ans = cur.fetchall()
pout(ans)

cur.execute("SELECT * FROM customers WHERE customerid = 'cust1001'")
ans = cur.fetchall()
pout(ans)

cur.execute("SELECT * FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
ans = cur.fetchall()
pout(ans)


cur.close()
conn.close()
