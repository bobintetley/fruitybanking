
# MySQL DB =============================
#import MySQLdb
#mysql_host = "localhost"
#mysql_user = "root"
#mysql_password = ""
#mysql_db = "fruitybanking"

# SQLite 3 DB ==========================
from pysqlite2 import dbapi2 as sqlite
# SQLite 2
#import sqlite 

# PostgresSQL ==========================
#from pyPgSQL import PgSQL
#pg_host = "localhost"
#pg_user = "user"
#pg_passwd = "pass"
    
def getConnection():
    """
        Creates a connection to the database and returns it
    """
    # MySQL
    #return MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_password, db=mysql_db )
    # SQLite
    #return PgSQL.connect(None, pg_user, pg_passwd, pg_host, "fruitybanking")
    return sqlite.connect("fruitybanking.db")
    
def runQuery(sql):
    """
        Runs the query given and returns the resultset
        as a grid of tuples
    """
    # Grab a connection and cursor
    c = getConnection()
    s = c.cursor()
    # Run the query and retrieve all rows
    s.execute(sql)
    d = s.fetchall()
    # Close the cursor and connection
    s.close()
    c.close()
    return d
    
def executeQuery(sql):
    """
        Runs the action query given
    """
    c = getConnection()
    s = c.cursor()
    s.execute(sql)
    c.commit()
    s.close()
    c.close()

def getId(table):
    """
        Returns the next ID in sequence for a table.
        Does this by basically doing a MAX on the ID
        field and returning that +1 (or 1 if the table
        has no records)
    """
    d = runQuery("SELECT Max(ID) FROM %s" % table)
    if (len(d) == 0) | (d[0][0] == None):
        return 1
    else:
        return d[0][0] + 1
   
   
