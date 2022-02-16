## Project 5: Object-Relational Mappings
### Due Feb 27, 2022, 11:59PM

*The assignment is to be done by yourself.*

Two parts: `psycopg` and `peewee`.

### Setup

As before we have created a VagrantFile for you. Start by doing `vagrant up` and `vagrant ssh` as usual.
Ensure that the Vagrantfile has loaded
the `flightsskewed` database, together with tables populated from  `large-skewed.sql`. Use
`flightsskewed` for all parts of this assignment.



**Part 1: External clients (2.5 pts)**:  One of more prominent ways to use a database system is using an
external client, using APIs such as ODBC and JDBC, or the
Python DB-API 2.0 specification.

We will be using the [psycopg](http://initd.org/psycopg/) instantiation of the Python DB spec to access the
database. There are many good tutorials, such as this
[Postgres/psycopg Tutorial](http://www.postgresqltutorial.com/postgresql-python),
the [default documentation](http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries) is quite good,
and you can also
get see a working example of queries in *SQLTesting.py* from Project 1.

For those new to Python, I recommend the
[Python Tutorial](https://docs.python.org/3/tutorial/index.html).

Your task to write a single Python function `runPsy()` function, in
file `psy.py`, that reads in a JSON file and updates the database
appropriately. `runPsy()` should take three parameters:
- `conn`: the database connection, already opened and initialized
- `curs`: a *cursor* for the connection. 
- `jsonFile`: the JSON file name

Database cursors implement the notion of a *session* with respect to a single
connection. Cursors are used to execute commands and return results, whether
one by one or all at once.

Each line in the input file will consist of a single JSON object in one of the following two formats:

- **New customer**, where information about a customer is provided in the following format
  (though our example file has each input in a single line). You can assume that the
  frequent flier airline name matches exactly what is there in the 'airlines' table.

```
{ "newcustomer": {
    "customerid": "cust1000", 
    "name": "XYZ", 
    "birthdate": "1991-12-06", 
    "frequentflieron": "Spirit Airlines"
  }
}
```

- **Flew On**, where information about the passengers in a flight is
provided. Create new rows in `flewon` for each customer, as well as the `customers`
table if the `customerid` does not already exist.
  - In some cases the `customerid` provided may not be present in the database (cust1000 as seen below). In this case, first update the `customers` table (all the info is guaranteed to be
there), and then add tuples to the `flewon` table.

```
{ "flewon": { 
    "flightid": "DL108", 
    "flightdate": "2015-09-25", 
    "customers": [ 
      {"customerid": "cust1001", "name": "XYZ", "birthdate": "1991-12-06", "frequentflieron": "AA"}, 
      {"customerid": "cust25"}, {"customerid": "cust33"} 
    ] 
  } 
}
```

### Testing

`python3 testPsy.py`

Notes:

1. In the case of either of the following errors, you should just print "Error424" and then exit. You do not need to handle any other errors.
  - If the `customerid` for a `newcustomer` update is already present, or
  - if the `frequentflieron` does not have a match in the airlines table
2. Be sure to *commit()* the database connection at the end. Otherwise, no data will be modified.
3. `example.json` is an example input file consisting of the JSON input
   above. We will test on a slightly different input file.
4. There are many Python JSON parsing libraries, but the simplest to use is the
[json module](https://docs.python.org/3/library/json.html) from the
[Python standard library](https://docs.python.org/3/library/).
5. `./clean-example.py` will remove the tuples added from `example.py`.


## Part 2: Object-Relational Mappings (`peewee`) (2.5 pts)

Another way to use a database is through an object-relational-mapping (ORM),
which maps table rows onto objects that are visible in a programming
language. The result is that you can write a database application without
using SQL at all.

We will re-write the previous program with exactly the same semantics, but using an object
model approach instead. There are many Python ORMs, including [Django](https://www.djangoproject.com/), but we
will use the simpler [Peewee](https://github.com/coleifer/peewee).

Your goal will to create a function `runOrm()`, parameterized by JSON
file name, and implements the same functionality as above.

Create your file by using a Peewee distribution tool called `pwiz`, which uses database
   *introspection* to create python classes mirroring an existing postgres schema. Use as follows:
```
    pwiz.py -e postgresql -u vagrant -P flightsskewed > orm.py
```
The password is `vagrant`. This will create the scaffolding of your ORM program in `orm.py`.

Test this code by replacing the database initialization with:
```
    database = PostgresqlDatabase('flightsskewed', **{'host': 'localhost', 'user': 'vagrant', 'password': 'vagrant'})
```
- Add `from datetime import date`  to the top of `orm.py`.
- Add the following lines to the end of the file:
```
    def runORM(jsonFile):
        Customers.delete().where(Customers.name == 'bob').execute()
        Airports.delete().where(Airports.airportid == 'PET').execute()
        
        bob = Customers(name="bob", customerid='cust1010', birthdate='1960-01-15', frequentflieron='SW')
        bob.save(force_insert=True)
    
        bwi = Airports(airportid='PET', city='Takoma', name='Pete', total2011=2, total2012=4)
        bwi.save(force_insert=True)
    
        for port in Airports.select().order_by(Airports.name):
            print (port.name)
```

Run by typing `python3 testORM.py` from the shell. You should have a record added to each of
*customers* and *airports*, followed by a listing of all airport
names. Verify that `bob` and `PET` were added using `psql`.

## Task: Replicate the work in `psy.py`.

Implement the same changes to 
the database as in `psy.py` (read JSON strings, insert corresponding tuples into the
database) in `runORM`, but do so entirely through the **Peewee** ORM interface.



## Notes
- You must add `.save(force_insert=True)` for new tuples or they will not be committed to the
  database.
- `python3 SQLTesting.py` is once again your last step. Run this and it will call both
  of your functions. Getting this to work means that your code will probably
  also work on Gradescope.
- You might or might not need to eliminate blank lines before "    class Meta:" lines in
   order to avoid syntax errors, i.e. get rid of any blank lines
   within class definitions (or ensure that proper indentation is maintained by adding spaces).

## Bonus Points
Add code at the bottom of `runORM` to update `NumberOfFlightsTaken` (already
created in `large-skewed.sql`) as in assign4. Worth 5 points on the first midterm.

## Submit Instructions
Submit `psy.py` and  `orm.py` files by compressing (zip, on a mac
select them both and right-click "select")  them to an archive with two
files, and then dropping that archive on to the <a href="https://www.gradescope.com/courses/336033/assignments/1688024">Assignment 5 submission</a>.
