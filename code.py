#!/usr/bin/python

import cherrypy
import datetime
import os, sys

import accounts
import html
import reports
import transactions

try:
    from sitedefs import NAMED_PERIOD
    period = "Income/expense totals shown for period: %s" % NAMED_PERIOD
except:
    period = ""

class Accounts:
    """
        The UI class
    """
    def index(self):
        """
            Index page of root.accounts - produces a list of all
            accounts with their codes, descriptions and balances
            with links to edit each account and view its transactions.
        """
        # Get the header
        h = html.getHTMLHeader("Accounts")
        
        # Header of account listings
        h = h + """
            <h2>Accounts</h2>
                <div id="menu"><ul id="nav">
                <li>%s</li>
                <li><img src="/static/plus.gif" /> <a href="/accounts/add" id="new-account">New Account</a></li>
                <li><a href="/reports">Reports</a></li><li></li></ul></div>
                <table width=100%%>
                  <thead>
                    <tr>
                        <th>Code</th>
                        <th>Type</th>
                        <th>Description</th>
                        <th align="right">Reconciled</th>
                        <th align="right">Balance</th>
                        <th align="right"></th>
                    </tr>
                </thead>
                <tbody>
            """ % period
            
        # Retrieve all the accounts
        acs = accounts.getAllAccounts()
        
        # The two alternating colours to use for the accounts
        light = "even"
        dark = "odd"
        bgcolor = light
	
        # Generate the HTML entries/links for each
        for a in acs:
	    # Current colour
            if (bgcolor == dark):
	        bgcolor = light
	    else:
	        bgcolor = dark
	
            h = h + """
                <tr class="%s">
                    <td><a href="/transactions/index?accountid=%s">%s</a></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td class="money">%s</td>
                    <td class="money">%s</td>
                    <td align="right"><a href="/accounts/reconcile?id=%s"><img alt="Reconcile" title="Mark transactions upto today as reconciled" border=0 src="/static/reconcile.png"></a><a href="/accounts/edit?id=%s"><img alt="Edit" title="Edit Account" border=0 src="/static/edit.png"></a><a href="/accounts/delete?id=%s"><img alt="Delete" title="Delete Account" border=0 src="/static/delete.png"></a></td>
                </tr>
                """ % (bgcolor, a.id, a.code, accounts.getAccountTypeForID(a.type), a.description, accounts.number_format(a.reconciledtotal), accounts.number_format(a.balance), a.id, a.id, a.id)
        # HTML footer
        h = h + """
                  </tbody>
                </table>
                """
        h = h + html.getHTMLFooter()
            
        return h
    
    def add(self):
        """
            Page to allow adding of a new account
        """
        h = html.getHTMLHeader("New Account")
        h = h + """
                <h2>New Account</h2>
                <form id="form1" method="post" action="/accounts/new">
                <table>
                    <tr>
                        <td>Code:</td>
                        <td><input name="code" type="text"/></td>
                    </tr>
                    <tr>
                        <td>Type:</td>
                        <td><select name="type">
                            %s
                        </select>
                    </tr>
                    <tr>
                        <td>Description:</td>
                        <td><textarea name="description"></textarea></td>
                    </tr>
                    <tr>
                        <td><input type="submit" value="submit"/></td>
                    </tr>
                </table>
        
                </form>
            """ % accounts.getAccountTypesAsHTML()
        h = h + html.getHTMLFooter()
        return h
        
    def edit(self, id):
        """
            Page to allow editing of an existing account.
        """
        # Grab the account
        a = accounts.getAccountById(id)
        # Build the HTML header
        h = html.getHTMLHeader("Edit Account %s (%s)" % (a.code, a.description))
        # Generate the form
        h = h + """
            <h2>Edit Account</h2>
            <form id="form1" method="post" action="/accounts/update">
            <table>
                <tr>
                    <td>Code:</td>
                    <td><input name="id" type="hidden" value="%s"/>
                        <input name="code" type="text" value="%s" /></td>
                </tr>
                <tr>
                        <td>Type:</td>
                        <td><select name="type">
                            %s
                        </select>
                    </tr>
                <tr>
                    <td>Description:</td>
                    <td><textarea name="description">%s</textarea></td>
                </tr>
                <tr>
                    <td><input type="submit" value="submit"/></td>
                </tr>
            </table>
            </form>
        """ % (a.id, a.code, accounts.getAccountTypesAsHTML(a.type), a.description)
        # Footer
        h = h + html.getHTMLFooter()
        return h

    def reconcile(self, id):
        """
    	Mark all transactions on an account as reconciled upto today's date.
    	"""
    	transactions.markAllTransactionsReconciled(id)
        raise cherrypy.HTTPRedirect("/accounts/index")

    def update(self, id, code, type, description):
        """
        Page to update an account and then return to
        the index page and the accounts list.
        """
        a = accounts.Account()
        a.id = id
        a.code = code
        a.type = type
        a.description = description
        accounts.updateAccount(a)
        raise cherrypy.HTTPRedirect("/accounts/index")

    def delete(self, id):
    	"""
	    Mark an account as deleted and return to the account list
	    """
        accounts.deleteAccount(id)
        raise cherrypy.HTTPRedirect("/accounts/index")

    def new(self, code, description, type):
        """
            Page to create a new account
        """
        a = accounts.Account()
        a.code = code
        a.description = description
        a.type = type
        accounts.createAccount(a)
        raise cherrypy.HTTPRedirect("/accounts/index")

    index.exposed = True
    add.exposed = True
    edit.exposed = True
    reconcile.exposed = True
    update.exposed = True
    delete.exposed = True
    new.exposed = True

class Transactions:
    """
        UI class for transaction functionality
    """
    def index(self, accountid, numToDisplay=20):
       
        if (type(numToDisplay) is unicode): numToDisplay = int(numToDisplay)
    	h = html.StringBuilder()
       
        h.add(html.getHTMLHeader("Transactions - %s" % accounts.getAccountById(accountid).code))
        
    	# Read how many we want to see from the session
        # numToDisplay = getNumberOfTrxToShow() 
	
        # Grab the transactions and balances for this account
        trx = transactions.getTransactions(accountid, numToDisplay)
        
        h.add ("<h2>Transactions - %s</h2>" % accounts.getAccountById(accountid).code)

        # Create the links to choose number of transactions
        links = ""
        if numToDisplay == 10:
            links = links + "10 "
        else:
            links = links + """<a href="/transactions/index?numToDisplay=10&accountid=%s">10</a> """ % accountid
        if numToDisplay == 20:
            links = links + "20 "
        else:
            links = links + """<a href="/transactions/index?numToDisplay=20&accountid=%s">20</a> """ % accountid
        if numToDisplay == 50:
            links = links + "50 "
        else:
            links = links + """<a href="/transactions/index?numToDisplay=50&accountid=%s">50</a> """ % accountid
        if numToDisplay == 100:
            links = links + "100 "
        else:
            links = links + """<a href="/transactions/index?numToDisplay=100&accountid=%s">100</a> """ % accountid
        if numToDisplay == -1:
            links = links + "All "
        else:
            links = links + """<a href="/transactions/index?numToDisplay=-1&accountid=%s">All</a> """ % accountid
        
        # Start table of transactions
        h.add("""
                <hr />
                <p>Show: %s</p>
                <form name="form1" method="post" action="/transactions/new">
                <table width="100%%">
                  <thead>
                    <tr>
                        <th>Date</th>
                        <th>R</th>
                        <th>Description</th>
                        <th>Account</th>
                        <th>Deposit</th>
                        <th>Withdrawal</th>
                        <th>Balance</th>
                        <th></th>
                    </tr>
                  </thead>
                """ % ( links ))
        
        # Calculate the range of the transactions we're actually going to display
        if numToDisplay == -1: numToDisplay = len(trx)
        rangestart = len(trx) - numToDisplay
        if rangestart < 0: rangestart = 0
        rangeend = len(trx)
        
        # Whether we've output a marker for today
        displayedToday = False
        
        # Alternate colours for the table rows, dark green, light green
        # and a pale yellow for editing
        dark = "even"
        light = "odd"
        editcolour = "editrow"
        
        bgcolor = dark
        
        # Javascript array of recent transaction descriptions and accounts
        jscript = "accounts = new Array();\ndescriptions = new Array();\n"
        ji = 0;
        for i in range(rangestart, rangeend):
            
            # Get the transaction
            t = trx[i]
            
            # Current colour
            if (bgcolor == dark): 
                bgcolor = light
            else:
                bgcolor = dark
               
            # Take the Python date and format it for display
            outputdate = transactions.pythonToDisplayDate(t.date)

            # Output "R" or a link to reconcile for reconciled
            if (t.reconciled == 1):
                outputreconciled = "R"
            else:
                outputreconciled = "<a href='/transactions/reconcile?id=%s&accountid=%s&numtodisplay=%d'>N</a>" % (t.id, accountid, numToDisplay)
                
            # Substitute withdrawal/deposit for a blank if it's 0 to
            # make things easier to read
            outputwithdrawal = ""
            outputdeposit = ""
            if (float(t.deposit) > 0):
                #outputdeposit = "%0.2f" % round(t.deposit, 2)
		        outputdeposit = transactions.number_format(t.deposit)
            if (float(t.withdrawal) > 0):
                #outputwithdrawal = "%0.2f" % round(t.withdrawal, 2)
		        outputwithdrawal = transactions.number_format(t.withdrawal)

            # Output the balance in red if it's overdrawn
            outputbalance = "%0.2f" % round(t.balance, 2)
             
            if float(t.balance) < 0:
                outputbalance = "<span class='negative'>%0.2f</span>" % round(t.balance, 2)

            # Is this the first date we've displayed that's
            # after today? If so, display a separator before outputting
            # so we have a visual cue of where today is
            if not displayedToday and t.date > datetime.date.today():
                h.add("""
                            <tr>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                                <td><hr color="red" size="1" noshade /></td>
                            </tr>
                        """)
                displayedToday = True
           
            # Output the transaction data
            h .add("""
                    <tr class="%s">
                        <td>%s</td>
                        <td class="reconciled">%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td class="money">%s</td>
                        <td class="money">%s</td>
                        <td class="money">%s</td>
                        <td>
                            <a href="/transactions/edit?id=%s&accountid=%s"><img alt="Edit" title="Edit Transaction" border=0 src="/static/edit.png"/></a>
                            <a href="/transactions/delete?id=%s&accountid=%s"><img alt="Delete" title="Delete Transaction" border=0 src="/static/delete.png"/></a>
                        </td>
                    </tr>
            """ % ( bgcolor, outputdate, outputreconciled, t.description, t.otheraccountcode, outputdeposit, outputwithdrawal, outputbalance, t.id, accountid, t.id, accountid ))
	    jscript += "accounts[%d] = \"%s\";\ndescriptions[%d] = \"%s\";\n" % (ji, t.otheraccountid, ji, t.description)
	    ji = ji + 1

        # Output the javascript array of transactions
        h.add("""<script language="javascript">
        %s
        nodesc = %d;
        function findaccount() {
            accountbox = document.form1.otheraccount;
            descriptionbox = document.form1.description;
            for (i = 0; i < nodesc; i++) {
                if (descriptions[i] == descriptionbox.value) {
                    for (j = 0; j < accountbox.length; j++) {
                        if (accountbox.options[j].value == accounts[i]) {
                            accountbox.selectedIndex = j;
                            break;
                        }
                    }
                }
            }
        }
        </script>""" % (jscript, ji))

        # Output form for creating a new transaction on the
        # end of the list.
        h.add("""
                <tr class=%s>
                    <td><input name="numtodisplay" type="hidden" value="%d"/>
                    <input id="datebox" name="date" size=10 value="%s"/></td>
                    <td><input name="reconciled" type="checkbox"/></td>
                    <td><input name="description" onChange="javascript:findaccount()" /></td>
                    <td><input name="account" type="hidden" value="%s"/>
                        <select name="otheraccount">%s</select></td>
                    <td class="editmoney"><input name="deposit" size=4/></td>
                    <td class="editmoney"><input name="withdrawal" size=4/></td>
                    <td><input type="submit" value="submit"></td>
                </tr>
            """ % ( editcolour, numToDisplay, transactions.getToday(), accountid, accounts.getAccountsAsHTML() ))
        
        # Finish up
        h.add("</form></table>")
        h.add("""
            <p><a href="/index">Back</a></p>
            """)

        # Scroll to the bottom of the screen and set focus to the date
        h.add("""
        <script type="text/javascript">
        window.scrollTo(0, document.body.scrollHeight);
        var t  = document.getElementById("datebox" );
        if (t !=null ) t.focus();
        </script>
        """)
        
        h.add(html.getHTMLFooter())
        
        return h.get()
        
    def new(self, date, reconciled = 0, description = "", account = 0, otheraccount = 0, deposit = 0, withdrawal = 0, numtodisplay = 20):
        """ 
            Called when a new transaction is submitted by the UI
        """
            
        # Create a new transaction object from data
        t = transactions.Transaction()
        t.accountid = account

        # Convert user date entered to Python date for object
        datebits = date.split("/")
        t.date = datetime.date(int(datebits[2]), int(datebits[1]), int(datebits[0]))
    
        t.reconciled = reconciled
        t.description = description
        t.otheraccountid = otheraccount
        if deposit != "": 
            t.deposit = deposit
        if withdrawal != "":
            t.withdrawal = withdrawal
        
        # Submit it for saving to the db
        transactions.createTransaction(t)
        
        # Redirect back to the transaction screen
        raise cherrypy.HTTPRedirect("/transactions/index?accountid=%s&numToDisplay=%d" % (account, int(numtodisplay)))
        
        
    def edit(self, id, accountid):
        """
            Screen to edit a transaction.
        """
        t = transactions.getTransactionById(id, accountid)
        outputdate = transactions.pythonToDisplayDate(t.date)
        h = html.getHTMLHeader("Edit Transaction")
        h = h + """
            <h2>Edit Transaction</h2>
            <form action="/transactions/update" method="post">
            <table>
                <tr>
                    <td>Date</td>
                    <td><input type="hidden" name="id" value="%s"/>
                        <input type="hidden" name="accountid" value="%s"/>
                        <input type="text" name="date" value="%s"/></td>
                </tr>
                <tr>
                    <td>Description</td>
                    <td><input type="text" name="description" value="%s"/></td>
                </tr>
                <tr>
                    <td>Account</td>
                    <td><select name="otheraccountid">%s</select></td>
                </tr>
                <tr>
                    <td>Deposit</td>
                    <td><input type="text" name="deposit" value="%s"/></td>
                </tr>
                <tr>
                    <td>Withdrawal</td>
                    <td><input type="text" name="withdrawal" value="%s"/></td>
                </tr>
                <tr>
                    <td>Reconciled</td>
                    <td><select name="reconciled">%s</select></td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type="submit" value="submit"/></td>
                </tr>
            </table>
            </form1>
            """ % ( id, accountid, outputdate, t.description, accounts.getAccountsAsHTML(t.otheraccountid), t.deposit, t.withdrawal, transactions.getReconciledAsHTML(t.reconciled) )
        
        h = h + html.getHTMLFooter()    
        
        return h


    def update(self, id, date, description, accountid, otheraccountid, deposit, withdrawal, reconciled):
        """
        Fired when the user updates an existing transaction
        """
        t = transactions.Transaction()
        t.id = id 
        t.date = transactions.displayToPythonDate(date)    
        t.description = description
        t.accountid = accountid
        t.otheraccountid = otheraccountid
        t.deposit = deposit
        t.withdrawal = withdrawal
        t.reconciled = reconciled
        transactions.updateTransaction(t)
        raise cherrypy.HTTPRedirect("/transactions/index?accountid=%s" % accountid)

    def showtrx(self, number, accountid):
        """
        UI page to change the number of transactions currently being
        viewed.
        """
        transactions.setNumberOfTrxToShow(int(number))
        raise cherrypy.HTTPRedirect("/transactions/index?accountid=%s" % accountid)
    

    def reconcile(self, id, accountid, numtodisplay):
        """
            Marks a transaction as reconciled
        """
        transactions.markTransactionReconciled(id)
        raise cherrypy.HTTPRedirect("/transactions/index?accountid=%s&numToDisplay=%d" % (accountid, int(numtodisplay)))

    def delete(self, id, accountid):
        """
            Deletes a transaction
        """
        transactions.deleteTransaction(id)
        raise cherrypy.HTTPRedirect("/transactions/index?accountid=%s" % accountid)

    index.exposed = True
    new.exposed = True
    edit.exposed = True
    update.exposed = True
    showtrx.exposed = True
    reconcile.exposed = True
    delete.exposed = True

class Reports:
    """
        CherryPy UI class for reporting functionality
    """
    def index(self):
        h = html.StringBuilder()
       
        h.add(html.getHTMLHeader("Reports"))
    	h.add("<h2>Reports</h2>");
    	h.add("""
		<form action="/reports/render" method="post">

		<p>Between: 
		<input name="datefrom" type="text" width="12" value="%s" /> 
		and 
		<input name="dateto" type="text" width="12" value="%s" />
		</p>
		<p>Report:
		<select name="report" size="8">
		<option selected value="INCEXP">Income and Expenditure</option>
		<option value="BALSH">Balance Sheet</option>
		<!--<option value="PAL">Profit and Loss</option>-->
		</select>
		<p><input type="submit" value="Prepare" /></p>
		<p><a href="/index">Back</a></p>
		</form>
	      """ % (transactions.getToday(), transactions.getToday()))
       
        h.add(html.getHTMLFooter()) 
        return h.get()

    def render(self, datefrom, dateto, report):
    	"""
    	Render the given report with a from/to date
    	"""
            
        # Check dates
        try:
            pyfrom = transactions.displayToPythonDate(datefrom)
            pyto = transactions.displayToPythonDate(dateto)
        except:
            return html.getHTMLHeader("Error") + "<p>Invalid date given.</p>" + html.getHTMLFooter()

        if report == "INCEXP":
            readabledate = datefrom + " - " + dateto
            return reports.incomeExpenditure(pyfrom, pyto, readabledate)
        if report == "BALSH":
            readabledate = "to " + dateto
            return reports.balanceSheet(pyto, readabledate)

    index.exposed = True
    render.exposed = True

       
root = Accounts()
root.accounts = Accounts()
root.reports = Reports()
root.transactions = Transactions()

conf = {
    '/': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': "static"
    }
}

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    #cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.server.socket_port = port
    cherrypy.quickstart(root, config = conf)

