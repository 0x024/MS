import MySQLdb
def dbconnect():
	conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='ubuntu',db='MS',charset="utf8")
	return conn
