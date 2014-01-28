#!/usr/bin/env python
import db
import transactions
import locale

#locale.setlocale(locale.LC_ALL, 'en_US')

def number_format(num, places=2):
    return locale.format("%.*f", (places, num), True)

class Account:
    """
        Account DTO
    """
    id = 0
    code = ""
    description = ""
    type = 0
    balance = 0
    reconciledtotal = 0

def getAllAccounts():
    """
        Returns a list of populated account objects from the
        database (and updates their balances at the same time).
    """
    
    # Retrieve all the account records
    d = db.runQuery("SELECT ID, Code, Description, Type FROM accounts WHERE Deleted=0 ORDER BY Type, Code")
    # Create the list we'll return
    l = []
    # Loop through the rows
    for row in range(len(d)):
        
        a = Account()
        a.id = d[row][0]
        a.code = d[row][1]
        a.description = d[row][2]
        a.type = d[row][3]
        a.balance = getAccountBalance(a.id)
        a.reconciledtotal = getReconciled(a.id)
        # Add this account to the list
        l.append(a)
    
    return l

def getAccountBalance(id):
    """
        Returns the balance for the given account id and
        based on the account type.
    """
    # Total withdrawals
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE SourceAccountID = %s AND Deleted = 0" % id)
    withdrawal = 0
    if (len(d) > 0):
        withdrawal = d[0][0]
    # Total deposits
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE DestinationAccountID = %s AND Deleted = 0" % id)
    deposit = 0
    if (len(d) > 0):
        deposit = d[0][0]
    if deposit == None:
        deposit = 0
    if withdrawal == None:
        withdrawal = 0
    # Round off to 2 dp
    deposit = round(deposit, 2)
    withdrawal = round(withdrawal, 2)
    # Produce the figure based on account type
    atype = db.runQuery("SELECT Type FROM accounts WHERE ID=%s" % id)
    t = int(atype[0][0]) 
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(round(deposit - withdrawal, 2))
    else:
	return round(deposit - withdrawal, 2)

def getAccountBalanceFromDate(id, fromdate):
    """
        Returns the balance for a given account from a certain date
	    (fromdate is expected in UNIX form)
    """
    # Total withdrawals
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE SourceAccountID = %s AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    withdrawal = 0
    if (len(d) > 0):
        withdrawal = d[0][0]
    # Total deposits
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE DestinationAccountID = %s AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    deposit = 0
    if (len(d) > 0):
        deposit = d[0][0]
    if deposit == None:
        deposit = 0
    if withdrawal == None:
        withdrawal = 0
    # Round off to 2 dp
    deposit = round(deposit, 2)
    withdrawal = round(withdrawal, 2)
    # Produce the figure based on account type
    atype = db.runQuery("SELECT Type FROM accounts WHERE ID=%s" % id)
    t = int(atype[0][0]) 
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(round(deposit - withdrawal, 2))
    else:
	return round(deposit - withdrawal, 2)

def getAccountBalanceToDate(id, todate):
    """
        Returns the balance for a given account upto (but not including) a certain date
	(todate is expected in UNIX form)
    """
    # Total withdrawals
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE SourceAccountID = %s AND Deleted = 0 AND Date < %s" % (id, todate))
    withdrawal = 0
    if (len(d) > 0):
        withdrawal = d[0][0]
    # Total deposits
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE DestinationAccountID = %s AND Deleted = 0 AND Date < %s" % (id, todate))
    deposit = 0
    if (len(d) > 0):
        deposit = d[0][0]
    if deposit == None:
        deposit = 0
    if withdrawal == None:
        withdrawal = 0
    # Round off to 2 dp
    deposit = round(deposit, 2)
    withdrawal = round(withdrawal, 2)
    # Produce the figure based on account type
    atype = db.runQuery("SELECT Type FROM accounts WHERE ID=%s" % id)
    t = int(atype[0][0]) 
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(round(deposit - withdrawal, 2))
    else:
	return round(deposit - withdrawal, 2)
 
def getReconciled(id):
    """
        Returns the reconciled balance for the given account id and
        based on the account type.
    """
    # Total withdrawals
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE SourceAccountID = %s AND Reconciled = 1 AND Deleted = 0" % id)
    withdrawal = 0
    if (len(d) > 0):
        withdrawal = d[0][0]
    # Total deposits
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE DestinationAccountID = %s AND Reconciled = 1 AND Deleted = 0" % id)
    deposit = 0
    if (len(d) > 0):
        deposit = d[0][0]
    if deposit == None:
        deposit = 0
    if withdrawal == None:
        withdrawal = 0
    # Round off to 2 dp
    deposit = round(deposit, 2)
    withdrawal = round(withdrawal, 2)
    # Produce the figure based on account type
    atype = db.runQuery("SELECT Type FROM accounts WHERE ID=%s" % id)
    t = int(atype[0][0]) 
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(round(deposit - withdrawal, 2))
    else:
        return round(deposit - withdrawal, 2)

def getReconciledFromDate(id, fromdate):
    """
        Returns the reconciled balance for the given account id and
        based on the account type from a certain date.
    """
    # Total withdrawals
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE SourceAccountID = %s AND Reconciled = 1 AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    withdrawal = 0
    if (len(d) > 0):
        withdrawal = d[0][0]
    # Total deposits
    d = db.runQuery("SELECT SUM(Amount) FROM trx WHERE DestinationAccountID = %s AND Reconciled = 1 AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    deposit = 0
    if (len(d) > 0):
        deposit = d[0][0]
    if deposit == None:
        deposit = 0
    if withdrawal == None:
        withdrawal = 0
    # Round off to 2 dp
    deposit = round(deposit, 2)
    withdrawal = round(withdrawal, 2)
    # Produce the figure based on account type
    atype = db.runQuery("SELECT Type FROM accounts WHERE ID=%s" % id)
    t = int(atype[0][0]) 
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(round(deposit - withdrawal, 2))
    else:
	return round(deposit - withdrawal, 2)

def getAccountById(id):
    """
        Returns an account object for the given account id
    """
    # Retrieve it
    d = db.runQuery("SELECT ID, Code, Description, Type FROM accounts WHERE ID = %s" % id)
    
    a = Account()
    a.id = d[0][0]
    a.code = d[0][1]
    a.description = d[0][2]
    a.type = d[0][3]
    a.balance = getAccountBalance(a.id)
    a.reconciledtotal = getReconciled(a.id)
        
    return a
    
def getAccountByCode(code):
    """
        Returns an account object for the given account code
    """
    # Retrieve it
    d = db.runQuery("SELECT ID, Code, Description, Type FROM accounts WHERE Code = '%s'" % code)
    
    a = Account()
    a.id = d[0][0]
    a.code = d[0][1]
    a.description = d[0][2]
    a.type = d[0][3]
    a.balance = getAccountBalance(a.id)
    a.reconciledtotal = getReconciled(a.id)
        
    return a
    
def updateAccount(accountObj):
    """
        Updates an existing account.
    """
    # Issue the update SQL
    db.executeQuery("UPDATE accounts SET Code='%s', Type=%s, Description='%s' WHERE ID = %s" % ( accountObj.code, accountObj.type, accountObj.description, accountObj.id ))
    
def createAccount(accountObj):
    """
        Creates a new account record and returns
        the id value of the newly created account.
    """
    aid = db.getId("accounts")
    db.executeQuery("INSERT INTO accounts (ID, Code, Description, Type, Deleted) VALUES (" + str(aid) + ",'" + accountObj.code + "', '" + accountObj.description + "', " + accountObj.type + ",0)")    
    
accounttypes = (
    ( 0, "Bank" ),
    ( 1, "Credit Card" ),
    ( 2, "Loan" ),
    ( 3, "Expense" ),
    ( 4, "Income" ),
    ( 5, "Pension" ),
    ( 6, "Shares" ),
	( 10, "Asset" ),
    ( 11, "Liability" )
)

def totalBalanceForPeriod(dateto, accounttype):
    """
        Returns a list of lists up to a given date and account
        type containing account codes and balances
    """
    udt = transactions.toUnixDate(dateto)
    accs = []
    d = db.runQuery("SELECT ID, Code FROM accounts WHERE Type = %s AND Deleted = 0" % str(accounttype))
    for ar in d:
        accs.append( [ ar[1], getAccountBalanceToDate(ar[0], udt) ] )
    return accs

def totalForPeriod(datefrom, dateto, accounttype, deposits = False):
    """
	    Returns a list of lists for a given period and account type.
	    [ [ accountcode, value ],  [ accountcode, value ] ]
	    If deposits is True, only includes transactions
	    with the account appearing in the DestinationAccountID
    """
    udf = transactions.toUnixDate(datefrom)
    udt = transactions.toUnixDate(dateto)
    accs = []
    d = db.runQuery("SELECT ID, Code FROM accounts WHERE Type = %s AND Deleted = 0" % str(accounttype))
    for ar in d:
        if deposits:
		    dt = db.runQuery("SELECT SUM(Amount) FROM trx WHERE Date >= %s AND Date <= %s AND DestinationAccountID = %s AND Deleted=0" % ( udf, udt, ar[0] ))
        else:
            dt = db.runQuery("SELECT SUM(Amount) FROM trx WHERE Date >= %s AND Date <= %s AND SourceAccountID = %s AND Deleted=0" % ( udf, udt, ar[0] ))
        dtotal = 0
        if (len(dt) > 0):
            dtotal = dt[0][0]
        if dtotal == None:
            dtotal = 0
        accs.append( [ ar[1], dtotal ])
    return accs

def deleteAccount(id):
    """
        Marks the given account as deleted
    """
    db.executeQuery("UPDATE accounts SET Deleted=1 WHERE ID=%s" % str(id))
    
def getAccountTypesAsHTML(selected = -1):
    """
        Returns HTML options representing the available account
        types. Optionally, you can pass the id of the selected item
    """
    
    s = ""
    for i in accounttypes:
        sel = ""
        if (i[0] == selected):
            sel = "selected "
        s = s + "<option %svalue='%s'>%s</option>" % ( sel, i[0], i[1])
        
    return s
    
def getAccountTypeForID(type):
    """
        Returns the account type text for a given id
    """
    for i in accounttypes:
        if i[0] == type:
            return i[1]
    return "Error"
    
def getAccountsAsHTML(selected = -1):
    """
        Returns HTML options representing the available
        accounts. Optionally, you can pass the id of the
        selected account.
    """
    
    s = ""
    for a in getAllAccounts():
        sel = ""
        if (a.id == selected):
            sel = "selected "
        s = s + "<option %svalue='%s'>%s</option>" % ( sel, a.id, a.code )
        
    return s
