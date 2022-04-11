from peewee import *
from datetime import date
import json

database = PostgresqlDatabase('flightsskewed', **{'host': 'localhost', 'user': 'vagrant', 'password': 'vagrant'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Airports(BaseModel):
    airportid = CharField(primary_key=True)
    city = CharField(null=True)
    name = CharField(null=True)
    total2011 = IntegerField(null=True)
    total2012 = IntegerField(null=True)

    class Meta:
        table_name = 'airports'

class Airlines(BaseModel):
    airlineid = CharField(primary_key=True)
    hub = ForeignKeyField(column_name='hub', field='airportid', model=Airports, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'airlines'

class Customers(BaseModel):
    birthdate = DateField(null=True)
    customerid = CharField(primary_key=True)
    frequentflieron = ForeignKeyField(column_name='frequentflieron', field='airlineid', model=Airlines, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'customers'

class Flights(BaseModel):
    airlineid = ForeignKeyField(column_name='airlineid', field='airlineid', model=Airlines, null=True)
    dest = ForeignKeyField(column_name='dest', field='airportid', model=Airports, null=True)
    flightid = CharField(primary_key=True)
    local_arrival_time = TimeField(null=True)
    local_departing_time = TimeField(null=True)
    source = ForeignKeyField(backref='airports_source_set', column_name='source', field='airportid', model=Airports, null=True)

    class Meta:
        table_name = 'flights'

class Flewon(BaseModel):
    customerid = ForeignKeyField(column_name='customerid', field='customerid', model=Customers, null=True)
    flightdate = DateField(null=True)
    flightid = ForeignKeyField(column_name='flightid', field='flightid', model=Flights, null=True)

    class Meta:
        table_name = 'flewon'

class Numberofflightstaken(BaseModel):
    customerid = CharField(null=True)
    customername = CharField(null=True)
    numflights = IntegerField(null=True)

    class Meta:
        table_name = 'numberofflightstaken'
        primary_key = False

def runORM(jsonFile):
    with open(jsonFile) as f:
        for line in f:               
            obj = json.loads(line)        
        
            if "newcustomer" in obj:
                newcustomer = obj["newcustomer"]
                (ff,) = Airlines.select(Airlines.airlineid).where(Airlines.name == newcustomer["frequentflieron"]).scalar(as_tuple=True)

                if not ff:
                    print("Error424")
                    exit()

                (customerExists,) = Customers.select((fn.COUNT(Customers.customerid) > 0)).where(Customers.customerid == newcustomer["customerid"]).scalar(as_tuple=True)  

                if not customerExists:
                    insertCust = Customers(name= newcustomer["name"], customerid= newcustomer["customerid"], birthdate= newcustomer["birthdate"], frequentflieron= ff)
                    insertCust.save(force_insert=True)
                else:
                    print("Error424")
                    exit()

            if "flewon" in obj:
                newflewon = obj["flewon"]
                for customer in newflewon["customers"]:
                    
                    (customerExists,) = Customers.select((fn.COUNT(Customers.customerid) > 0)).where(Customers.customerid == customer["customerid"]).scalar(as_tuple=True)

                    if not customerExists:
                        insertCust = Customers(name= customer["name"], customerid= customer["customerid"], birthdate= customer["birthdate"], frequentflieron= customer["frequentflieron"])
                        insertCust.save(force_insert=True)

                    
                    insertFlew = Flewon(flightid= newflewon["flightid"], customerid= customer["customerid"], flightdate= newflewon["flightdate"])
                    insertFlew.save(force_insert=True)


            

