import os

from django.conf import settings
from pymongo import MongoClient
import MySQLdb

db = MySQLdb.connect("192.168.2.6", "root", "123456", "sr")

def MigrateToMongo(sql_relation):
	cur = db.cursor()
	fields  = []
	cur.execute("desc" + sql_relation)

	for row in cur.fetchall():
		fields.append(row[0])

	monglo_db = settings.MONGO_DB_CONN
	if sql_relation is "SuperReceptionist_callrecord":		
		cur.execute("select * from SuperReceptionist_callrecord order by start_time desc limit 1000")
	elif sql_relation is "backgridtest_callrecordpreference":
		cur.execute("select * from backgridtest_callrecordpreference")
	for row in cur.fetchall():
		options  = {}
		for index, field in enumerate(row):
			options[fields[index]] = field
		
		options["_id"] = row[0]
		options.pop("id")
		monglo_db.call_records.insert(options)

MigrateToMongo("SuperReceptionist_callrecord")
MigrateToMongo("backgridtest_callrecordpreference")