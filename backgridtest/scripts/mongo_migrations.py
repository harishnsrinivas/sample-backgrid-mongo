import os

from pymongo import MongoClient
from datetime import datetime
import MySQLdb
import logging

LOGGING_LEVEL               = logging.DEBUG
LOGGING_FILE                = '/var/log/migrate_to_mongo.log'


def getMongoConnection():
    mongo_client = MongoClient()
    return mongo_client.db4backgrid

MONGO_DB_CONN = getMongoConnection()


db = MySQLdb.connect("192.168.2.6", "root", "123456", "sr")

def ResultItertator(cur, max_size=2000000):
    i=1
    while True:
        rows = cur.fetchmany(max_size)
        print len(rows)
        if not rows:
            break
        else:
            for row in rows:
                yield row
            print i
            i+=1



def MigrateToMongo(sql_relation):

    start_time = datetime.utcnow()
    
    logging.info("migration process started")
    logging.basicConfig(
        filename=LOGGING_FILE,
        format='%(levelname)s : %(asctime)s - %(message)s',
        level=LOGGING_LEVEL
    )

    # Keep column names in an array

    cur = db.cursor()
    fields  = []
    cur.execute("desc " + sql_relation)

    #only desc, so fetchall is not a suicide!

    for row in cur.fetchall():
        fields.append(row[0])


    #Migrating call records, fetchall here = SUICIDE.

    if sql_relation is "SuperReceptionist_callrecord":      
        cur.execute("select * from SuperReceptionist_callrecord")
    elif sql_relation is "backgridtest_callrecordpreference":
        cur.execute("select * from backgridtest_callrecordpreference")

    for row in ResultItertator(cur):
        options  = {}
        for index, field in enumerate(row):
            options[fields[index]] = field

        options["_id"] = row[0]
        options.pop("id")
        MONGO_DB_CONN.call_records4.insert(options)

    print "ENDDD"

    end_time = datetime.utcnow()
    time_consumed = end_time - start_time
    logging.info("Total time consumed : %s seconds" %(time_consumed.total_seconds()))

    print "Total time : %s" %(time_consumed.total_seconds())

if __name__ == "__main__":
    MigrateToMongo("SuperReceptionist_callrecord")
    #MigrateToMongo("backgridtest_callrecordpreference")

