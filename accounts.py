#!/usr/bin/env python
import db
import transactions

try:
    from sitedefs import ACCOUNTING_PERIOD
    has_period = True
except:
    has_period = False

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
    d = db.runQuery("SELECT id, code, description, type FROM accounts WHERE deleted=0 ORDER BY type, code")
    # Create the list we'll return
    l = []
    # Loop through the rows
    for row in d:
        
        a = Account()
        a.id = row.id
        a.code = row.code
        a.description = row.description
        a.type = row.type
        if has_period and a.type in (3, 4):
            a.balance = getAccountBalanceFromDate(a.id, ACCOUNTING_PERIOD)
            a.reconciledtotal = getReconciledFromDate(a.id, ACCOUNTING_PERIOD)
        else:
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
    withdrawal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE SourceAccountID = %s AND Deleted = 0" % id)
    # Total deposits
    deposit = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE DestinationAccountID = %s AND Deleted = 0" % id)
    # Produce the figure based on account type
    t = db.first("SELECT Type AS first FROM accounts WHERE id=%s" % id)
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(deposit - withdrawal)
    else:
	return deposit - withdrawal

def getAccountBalanceFromDate(id, fromdate):
    """
        Returns the balance for a given account from a certain date
	    (fromdate is expected in UNIX form)
    """
    # Total withdrawals
    withdrawal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE SourceAccountID = %s AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    # Total deposits
    deposit = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE DestinationAccountID = %s AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    # Produce the figure based on account type
    t = db.first("SELECT Type AS first FROM accounts WHERE id=%s" % id)
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(deposit - withdrawal)
    else:
	return deposit - withdrawal

def getAccountBalanceToDate(id, todate):
    """
        Returns the balance for a given account upto (but not including) a certain date
	(todate is expected in UNIX form)
    """
    # Total withdrawals
    withdrawal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE SourceAccountID = %s AND Deleted = 0 AND Date < %s" % (id, todate))
    # Total deposits
    deposit = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE DestinationAccountID = %s AND Deleted = 0 AND Date < %s" % (id, todate))
    # Produce the figure based on account type
    t = db.first("SELECT Type AS first FROM accounts WHERE id=%s" % id)
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(deposit - withdrawal)
    else:
    	return deposit - withdrawal
 
def getReconciled(id):
    """
        Returns the reconciled balance for the given account id and
        based on the account type.
    """
    # Total withdrawals
    withdrawal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE SourceAccountID = %s AND Reconciled = 1 AND Deleted = 0" % id)
    # Total deposits
    deposit = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE DestinationAccountID = %s AND Reconciled = 1 AND Deleted = 0" % id)
    # Produce the figure based on account type
    t = db.first("SELECT Type AS first FROM accounts WHERE id=%s" % id)
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(deposit - withdrawal)
    else:
        return deposit - withdrawal

def getReconciledFromDate(id, fromdate):
    """
        Returns the reconciled balance for the given account id and
        based on the account type from a certain date.
    """
    # Total withdrawals
    withdrawal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE SourceAccountID = %s AND Reconciled = 1 AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    # Total deposits
    deposit = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE DestinationAccountID = %s AND Reconciled = 1 AND Deleted = 0 AND Date >= %s" % (id, fromdate))
    # Produce the figure based on account type
    t = db.first("SELECT Type AS first FROM accounts WHERE id=%s" % id)
    # Income and expense accounts should always be positive, the others
    # will be correct for deposit/withdrawal
    if t == 3 or t == 4:
        return abs(deposit - withdrawal)
    else:
	return deposit - withdrawal

def getAccountById(id):
    """
        Returns an account object for the given account id
    """
    # Retrieve it
    d = db.runQuery("SELECT id, code, description, type FROM accounts WHERE id = %s" % id)
    a = Account()
    a.id = d[0].id
    a.code = d[0].code
    a.description = d[0].description
    a.type = d[0].type
    a.balance = getAccountBalance(a.id)
    a.reconciledtotal = getReconciled(a.id)
    return a
    
def getAccountByCode(code):
    """
        Returns an account object for the given account code
    """
    # Retrieve it
    d = db.runQuery("SELECT id, code, description, type FROM accounts WHERE code = '%s'" % code)
    a = Account()
    a.id = d[0].id
    a.code = d[0].code
    a.description = d[0].description
    a.type = d[0].type
    a.balance = getAccountBalance(a.id)
    a.reconciledtotal = getReconciled(a.id)
    return a
    
def updateAccount(accountObj):
    """
        Updates an existing account.
    """
    # Issue the update SQL
    db.db.update("accounts", code=accountObj.code, type=accountObj.type, description=accountObj.description, where="id=%d" % int(accountObj.id))
    
def createAccount(accountObj):
    """
        Creates a new account record and returns
        the id value of the newly created account.
    """
    aid = db.getId("accounts")
    db.db.insert("accounts", id=aid, code=accountObj.code, type=accountObj.type, description=accountObj.description, deleted=0)
    return aid
    
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
    d = db.runQuery("SELECT id, code FROM accounts WHERE type = %s AND deleted = 0" % str(accounttype))
    for ar in d:
        accs.append( [ ar.code, getAccountBalanceToDate(ar.id, udt) ] )
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
    d = db.runQuery("SELECT id, code FROM accounts WHERE type = %s AND deleted = 0" % str(accounttype))
    for ar in d:
        if deposits:
		    dtotal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE Date >= %s AND Date <= %s AND DestinationAccountID = %s AND Deleted=0" % ( udf, udt, ar.id ))
        else:
            dtotal = db.sumQuery("SELECT SUM(Amount) AS total FROM trx WHERE Date >= %s AND Date <= %s AND SourceAccountID = %s AND Deleted=0" % ( udf, udt, ar.id ))
        accs.append( [ ar.code, dtotal ])
    return sorted(accs, key=lambda x:x[0])

def deleteAccount(id):
    """
        Marks the given account as deleted
    """
    db.db.update("accounts", deleted=1, where="id=%d" % int(id))
    
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
