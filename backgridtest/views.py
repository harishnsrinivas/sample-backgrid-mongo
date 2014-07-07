import MySQLdb

from pymongo import MongoClient

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


def renderTestGrid(request):
	return render(request, "index.html")

def renderConfigPage(request):
	return render(request, "savepref.html")

def initcdrlist(request):
	print "INSIDE INTICDRLIST"
	db = settings.MONGO_DB_CONN
	cdr_collection = db.cdrs
	cdr_pref = db.cdrpref
	cdr_list = []
	for i in range(10):
		cdr_list.append({"Name":"cdr-%s"%(i), "Purpose":i })
	cdr_collection.insert(cdr_list)

def migratecdr(request):
	db = MySQLdb.connect("192.168.2.6", "root", "123456", "sr")
	cur = db.cursor()
	fields  = []

	cur.execute("desc SuperReceptionist_callrecord")

	for row in cur.fetchall():
		fields.append(row[0])

	monglo_db = settings.MONGO_DB_CONN

	cur.execute("select * from SuperReceptionist_callrecord order by start_time desc limit 1000")
	for row in cur.fetchall():
		options  = {}
		for index, field in enumerate(row):
			options[fields[index]] = field
		
		options["_id"] = row[0]
		options.pop("id")
		
		monglo_db.call_records.insert(options)

	return HttpResponse("your request is under process")