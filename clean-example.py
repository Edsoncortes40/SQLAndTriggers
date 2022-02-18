#!/usr/bin/python3
import psycopg2
import os
import sys
import subprocess

conn = psycopg2.connect("dbname=flightsskewed user=vagrant")
cur = conn.cursor()

# cleanup
cur.execute("DELETE FROM flewon WHERE flightid='DL108' AND flightdate='2015-09-25'")
cur.execute("DELETE FROM flewon WHERE customerid >= 'cust1000' AND LENGTH(customerid) = 8")
cur.execute("DELETE FROM customers WHERE customerid >= 'cust1000' AND LENGTH(customerid) = 8")
conn.commit()
