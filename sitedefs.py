
import datetime, transactions

ACCOUNTING_PERIOD = transactions.toUnixDate(datetime.date(2013, 4, 1))
NAMED_PERIOD = "1st April 2013 - 31st March 2014"
SHOW_VAT = True

DB_TYPE = "sqlite"
DB_NAME = "fruitybanking.db"
DB_USER = ""
DB_PASSWORD = ""

#DB_TYPE = "postgres"
#DB_NAME = "banking"
#DB_USER = "user"
#DB_PASSWORD = "password"

