#!/usr/bin/env python

import datetime, transactions

ACCOUNTING_PERIOD = transactions.toUnixDate(datetime.date(2013, 04, 01))
NAMED_PERIOD = "1st April 2013 - 31st March 2014"

DB_TYPE = "sqlite"
DB_NAME = "fruitybanking.db"
DB_USER = ""
DB_PASSWORD = ""

#DB_TYPE = "postgres"
#DB_NAME = "banking"
#DB_USER = "user"
#DB_PASSWORD = "password"

