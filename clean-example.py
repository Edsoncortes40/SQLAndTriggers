#!/usr/bin/python3
import psycopg2
import os
import sys
import subprocess

conn = psycopg2.connect("dbname=flightsskewed user=vagrant")
cur = conn.cursor()

# cleanup
cur.execute("delete from flewon where flightid='DL108' and flightdate='2015-09-25'")
cur.execute("delete from customers where customerid='cust1000'")
cur.execute("delete from customers where customerid='cust1001'")

conn.commit()
