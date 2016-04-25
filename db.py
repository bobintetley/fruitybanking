#!/usr/bin/python

# Shared global connection
db = None

def runQuery(sql):
    return db.query(sql).list()

def sumQuery(sql):
    rv = 0.0
    rows = db.query(sql)
    for r in rows:
        if type(r.total) == float:
            rv = r.total
            break
    return rv

def first(sql):
    rv = 0
    rows = db.query(sql)
    for r in rows:
        rv = r.first
        break
    return rv

def executeQuery(sql):
    return db.execute(sql)

def getId(table):
    """
        Returns the next ID in sequence for a table.
        Does this by basically doing a MAX on the ID
        field and returning that +1 (or 1 if the table
        has no records)
    """
    d = db.query("SELECT Max(ID) AS maxid FROM %s" % table)[0].maxid
    if d is None: return 1
    return d + 1

