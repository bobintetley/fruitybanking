#!/usr/bin/python

import datetime
import accounts
import transactions

# Demonstration of how payments can be scripted.
# Eg: Pay 500 from our Current account to the Mortgage account

current_account = accounts.getAccountByCode("Current")
mortgage_account = accounts.getAccountByCode("Mortgage")

t = transactions.Transaction()
t.date = datetime.date.today()
t.description = "Mortgage payment"
t.reconciled = 0
t.accountid = current_account.id
t.otheraccountid = mortgage_account.id
deposit = 0
withdrawal = 500
transactions.createTransaction(t)

