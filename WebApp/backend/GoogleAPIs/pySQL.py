#!/usr/bin/python3

import pymysql
import mainNLP

#database access information
username ='watchmtladmin'
password ='watchmtl123'
hostname ='jamesgtang.com'
database ='WatchMTL'

def getMsg(id):

	db = pymysql.connect(hostname,username,password,database)
	cursor=db.cursor()
	query = "SELECT message FROM client WHERE id='%s'"
	cursor.execute(query,id)
	results = cursor.fetchall()
	for row in results:
		msg = row[0]
	return msg	
	cursor.close()
# this method does not work
def parseMsg(msg,id):
	print("Msf is",msg)
	response= mainNLP.process_input(msg)
	db = pymysql.connect(hostname,username,password,database)
	cursor=db.cursor()
	print("Response is",response)
	query = "UPDATE client SET keyword='%s' WHERE id='%s'"
	cursor.execute(query,(str(response),id))
	db.commit()