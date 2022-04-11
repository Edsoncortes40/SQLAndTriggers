#!/usr/bin/python3
import psycopg2
import json
import sys
from types import *

def runPsy(conn, curs, jsonFile):
    with open(jsonFile) as f:
        for line in f:               
            obj = json.loads(line)        
        
            if "newcustomer" in obj:
                newcustomer = obj["newcustomer"]
                ffosql = """select airlineid
                            from airlines
                            where name = %s ;"""
                curs.execute(ffosql, (newcustomer['frequentflieron'], ))
                frequentflieron = curs.fetchone()

                if not frequentflieron:
                    print("Error424")
                    exit()
                else:
                    (ff,) = frequentflieron

                sql1 = """select (count(*) > 0) from customers where customerid = %s"""
                curs.execute(sql1, (newcustomer["customerid"],)) 
                (customerExists,)  = curs.fetchone() 

                if not customerExists:
                    sqlInsert = """INSERT INTO customers(customerid, name, birthdate, frequentflieron)
                                   VALUES(%s, %s, %s, %s);"""
                    curs.execute(sqlInsert, (newcustomer["customerid"], newcustomer["name"], newcustomer["birthdate"], ff))
                else:
                    print("Error424")
                    exit()

            if "flewon" in obj:
                newflewon = obj["flewon"]
                for customer in newflewon["customers"]:

                    sql1 = """select (count(*) > 0) from customers where customerid = %s"""
                    curs.execute(sql1, (customer["customerid"],))
                    (customerExists,)  = curs.fetchone() 

                    if not customerExists:
                        insertCust = """INSERT INTO customers(customerid, name, birthdate, frequentflieron)
                                        VALUES(%s, %s, %s, %s);"""
                        curs.execute(insertCust, (customer["customerid"], customer["name"], customer["birthdate"], customer["frequentflieron"]))


                    insertFlew = """INSERT INTO flewon(flightid, customerid, flightdate)
                                    VALUES(%s,%s, %s);"""
                    curs.execute(insertFlew, (newflewon["flightid"], customer["customerid"], newflewon["flightdate"]))    
                    
        conn.commit()
        

