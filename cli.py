#!/usr/bin/env python3

import os, sys, re, datetime

"""
FruityBanking command line interface for viewing and adding transactions.
"""

PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
sys.path.append(PATH)

import accounts
import db
import transactions
import web
from sitedefs import SHOW_VAT, DB_TYPE, DB_NAME, DB_USER, DB_PASSWORD

web.config.debug = False
if DB_TYPE == "postgres" or DB_TYPE == "mysql":
    db.db = web.database(dbn=DB_TYPE, db=DB_NAME, user=DB_USER, pw=DB_PASSWORD)
else:
    if not DB_NAME.startswith("/"): DB_NAME = "%s%s" % (PATH, DB_NAME)
    db.db = web.database(dbn="sqlite", db=DB_NAME)

def currency_out(num):
    return "£%0.2f" % (int(num) / 100.0)

def spaceleft(s, spaces):
    """
    leftpads a string to a number of spaces
    """
    sp = " "*255
    if len(s) > spaces: return s
    nr = spaces - len(s)
    return sp[0:nr] + s

def spaceright(s, spaces):
    """
    rightpads a string to a number of spaces
    """
    sp = " "*255
    if len(s) > spaces: return s
    nr = spaces - len(s)
    return s + sp[0:nr]

def ascii_table(data, separator=" | "):
    """
    Given a 2D array of table values, outputs them as an ASCII table.
    Columns are sized to the widest value.
    """
    # Iterate the data once to find the widest value in each column
    colwidths = [0] * len(data[0]) # initialise a 0 for each column
    for row in data:
        for i, v in enumerate(row):
            if len(v) > colwidths[i]:
                colwidths[i] = len(v)
    # Calculate the total width
    totalwidth = 0
    for c in colwidths:
        totalwidth += c
    totalwidth += len(colwidths) * len(separator) # add separators to the width
    # Build output
    buffer = []
    for ri, row in enumerate(data):
        for i, v in enumerate(row):
            # Right align money, Left align strings
            if v.find("£") != -1:
                buffer.append(spaceleft(v, colwidths[i]))
            else:
                buffer.append(spaceright(v, colwidths[i]))
            # Leave a separator between columns if this isn't the last column
            if i != len(colwidths)-1:
                buffer.append(separator)
        buffer.append("\n")
        if ri == 0:
            buffer.append("-" * (totalwidth-1))
            buffer.append("\n")
    return "".join(buffer)

def show_accounts():
    """
    Output the list of accounts and balances.
    """
    try:
        # Show account period if one is set
        from sitedefs import NAMED_PERIOD
        period = "Income/expense totals shown for period: %s" % NAMED_PERIOD
        print(period)
        print("")
    except:
        period = ""
    header = [ "ID", "Code", "Type", "Description", "Reconciled", "Balance" ]
    data = [ header ]
    acs = accounts.getAllAccounts()
    for a in acs:
        data.append([ str(a.id), a.code, accounts.getAccountTypeForID(a.type), a.description, currency_out(a.reconciledtotal), currency_out(a.balance) ])
    print(ascii_table(data))

def show_trx(accountid, datefrom="", dateto=""):
    """
    Output the list of transactions for an account.
    """
    d31 = datetime.timedelta(days = 31)
    if dateto == "": 
        dto = transactions.toUnixDate(datetime.datetime.today() + d31)
        dateto = transactions.pythonToDisplayDate(datetime.datetime.today() + d31)
    else:
        dto = transactions.toUnixDate(transactions.displayToPythonDate(dateto))
    if datefrom == "": 
        dfrom = transactions.toUnixDate(datetime.datetime.today() - d31)
        datefrom = transactions.pythonToDisplayDate(datetime.datetime.today() - d31)
    else:
        dfrom = transactions.toUnixDate(transactions.displayToPythonDate(data.datefrom))
    trx = transactions.getTransactions(accountid, dfrom, dto)
    print("Transactions - %s (%s): %s to %s" % (accounts.getAccountById(accountid).code, accountid, datefrom, dateto))
    print("")
    header = [ "Date", "R", "V", "Description", "Account", "Deposit", "Withdrawal", "Balance" ]
    data = [ header ]
    displayedToday = False
    for t in trx:
        outputdate = transactions.pythonToDisplayDate(t.date)
        outputreconciled = t.reconciled == 1 and "R" or ""
        outputvat = t.vat == 1 and "V" or ""
        outputwithdrawal = ""
        outputdeposit = ""
        if t.deposit > 0:
            outputdeposit = currency_out(t.deposit)
        if t.withdrawal > 0:
            outputwithdrawal = currency_out(t.withdrawal)
        outputbalance = currency_out(t.balance)
        if not displayedToday and t.date > datetime.date.today():
            displayedToday = True
            data.append([ "--", "--", "--", "--", "--", "--", "--", "--" ])
            pass # TODO: display horizontal bar
        # highlight bad transactions where source/dest are the same
        outputotheraccount = "%s (%s)" % (t.otheraccountcode, t.otheraccountid)
        if t.otheraccountid == int(accountid):
            outputotheraccount = "<--> %s" % outputotheraccount
        data.append([ outputdate, outputreconciled, outputvat, t.description, outputotheraccount, outputdeposit,
            outputwithdrawal, outputbalance ])
    print(ascii_table(data))

if len(sys.argv) == 1:
    show_accounts()

if len(sys.argv) == 2 and sys.argv[1] == "help":
    print("Usage:")
    print("   cli [no args]")
    print("   cli trx <accountid>")
    print("   cli trx <accountid> 2022-05-01 2022-06-01")

if len(sys.argv) == 3 and sys.argv[1] == "trx":
    show_trx(sys.argv[2])

if len(sys.argv) == 5 and sys.argv[1] == "trx":
    show_trx(sys.argv[2], sys.argv[3], sys.argv[4])

