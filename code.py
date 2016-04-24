#!/usr/bin/python

import datetime
import os, sys

import accounts
import html
import json
import reports
import transactions
import web

PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
sys.path.append(PATH)

urls = (
    "/", "account",
    "/index", "account",
    "/account_add", "account_add",
    "/account_reconcile", "account_reconcile",
    "/account_edit", "account_edit",
    "/account_delete", "account_delete",
    "/transaction", "transaction",
    "/transaction_add", "transaction_add",
    "/transaction_reconcile", "transaction_reconcile", 
    "/transaction_edit", "transaction_edit",
    "/transaction_delete", "transaction_delete",
    "/report", "report",
    "/report_render", "report_render"
)

app = web.application(urls, globals())
application = app.wsgifunc()

class account:
    def GET(self):
        """
            Index page of root.accounts - produces a list of all
            accounts with their codes, descriptions and balances
            with links to edit each account and view its transactions.
        """
        # Get the header
        h = html.getHTMLHeader("Accounts")
        # Get an account period if one is set
        try:
            from sitedefs import NAMED_PERIOD
            period = "Income/expense totals shown for period: %s" % NAMED_PERIOD
        except:
            period = ""
        # Header of account listings
        h = h + """
            <h2>Accounts</h2>
                <div id="menu"><ul id="nav">
                <li>%s</li>
                <li><img src="/static/plus.gif" /> <a href="account_add" id="new-account">New Account</a></li>
                <li><a href="report">Reports</a></li><li></li></ul></div>
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
                    <td><a href="transaction?accountid=%s">%s</a></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td class="money">%s</td>
                    <td class="money">%s</td>
                    <td align="right"><a href="account_reconcile?id=%s"><img alt="Reconcile" title="Mark transactions upto today as reconciled" border=0 src="/static/reconcile.png"></a><a href="account_edit?id=%s"><img alt="Edit" title="Edit Account" border=0 src="/static/edit.png"></a><a href="account_delete?id=%s"><img alt="Delete" title="Delete Account" border=0 src="/static/delete.png"></a></td>
                </tr>
                """ % (bgcolor, a.id, a.code, accounts.getAccountTypeForID(a.type), a.description, accounts.number_format(a.reconciledtotal), accounts.number_format(a.balance), a.id, a.id, a.id)
        # HTML footer
        h = h + """
                  </tbody>
                </table>
                """
        h = h + html.getHTMLFooter()
            
        return h
   
class account_add:
    def GET(self):
        """
            Page to allow adding of a new account
        """
        h = html.getHTMLHeader("New Account")
        h = h + """
                <h2>New Account</h2>
                <form id="form1" method="post" action="account_add">
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

    def POST(self):
        """
            Page to create a new account
        """
        data = web.input()
        a = accounts.Account()
        a.code = data.code
        a.description = data.description
        a.type = data.type
        accounts.createAccount(a)
        raise web.seeother("index")

class account_edit:
    def GET(self):
        """
            Page to allow editing of an existing account.
        """
        data = web.input(id = 0)
        # Grab the account
        a = accounts.getAccountById(data.id)
        # Build the HTML header
        h = html.getHTMLHeader("Edit Account %s (%s)" % (a.code, a.description))
        # Generate the form
        h = h + """
            <h2>Edit Account</h2>
            <form id="form1" method="post" action="account_edit">
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

    def POST(self):
        """
        Page to update an account and then return to
        the index page and the accounts list.
        """
        data = web.input()
        a = accounts.Account()
        a.id = data.id
        a.code = data.code
        a.type = data.type
        a.description = data.description
        accounts.updateAccount(a)
        raise web.seeother("index")

class account_reconcile:
    def GET(self):
        """
    	Mark all transactions on an account as reconciled upto today's date.
    	"""
        data = web.input(id = 0)
    	transactions.markAllTransactionsReconciled(data.id)
        raise web.seeother("index")

class account_delete:
    def GET(self):
    	"""
	    Mark an account as deleted and return to the account list
	    """
        data = web.input(id = 0)
        accounts.deleteAccount(data.id)
        raise web.seeother("index")

class transaction:
    def GET(self):
        """
            UI class for transaction functionality
        """
        data = web.input(accountid = 0, dateto = "", datefrom = "")
        accountid = data.accountid
    	h = html.StringBuilder()
        d31 = datetime.timedelta(days = 31)
       
        h.add(html.getHTMLHeader("Transactions - %s" % accounts.getAccountById(accountid).code))

        dateto = data.dateto
        datefrom = data.datefrom
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
        
        # Grab the transactions and balances for this account
        trx = transactions.getTransactions(accountid, dfrom, dto)
        
        h.add ("<h2>Transactions - %s</h2>" % accounts.getAccountById(accountid).code)

        # Start table of transactions
        h.add("""
                <hr />
                <form action="transaction" method="get">
                <p>Transactions from: 
                <input type="hidden" name="accountid" value="%s" />
                <input id="datefrom" name="datefrom" size="12" value="%s" /> 
                to <input id="dateto" name="dateto" size="12" value="%s" />
                <input id="filterdate" type="submit" value="Show"/>
                </p>
                </form>
                <script>
                $(function() {
                    $("#datefrom, #dateto").datepicker({ dateFormat: "dd/mm/yy" });
                    $("#filterdate").button();
                });
                </script>
                <form name="form1" method="post" action="transaction_add">
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
                """ % ( accountid, data.datefrom, data.dateto ))
        
        # Whether we've output a marker for today
        displayedToday = False
        
        # Alternate colours for the table rows, dark green, light green
        # and a pale yellow for editing
        dark = "even"
        light = "odd"
        editcolour = "editrow"
        
        bgcolor = dark
        
        desctoaccount = {}
        descs = []
        for i in xrange(0, len(trx)):
            
            # Get the transaction
            t = trx[i]
           
            # Map description to an account id
            desctoaccount[t.description] = t.otheraccountid
            descs.append(t.description)

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
                outputreconciled = "<a href='transaction_reconcile?id=%s&accountid=%s'>N</a>" % (t.id, accountid)
                
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

            # If we have a cancelling transaction (both sides the same)
            # highlight the account to show the error
            outputotheraccount = t.otheraccountcode
            if t.otheraccountid == int(accountid):
                outputotheraccount = "<span style='color: red'>%s</span>" % outputotheraccount
           
            # Output the transaction data
            h.add("""
                    <tr class="%s">
                        <td>%s</td>
                        <td class="reconciled">%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td class="money">%s</td>
                        <td class="money">%s</td>
                        <td class="money">%s</td>
                        <td>
                            <a href="transaction_edit?id=%s&accountid=%s"><img alt="Edit" title="Edit Transaction" border=0 src="/static/edit.png"/></a>
                            <a href="transaction_delete?id=%s&accountid=%s"><img alt="Delete" title="Delete Transaction" border=0 src="/static/delete.png"/></a>
                        </td>
                    </tr>
            """ % ( bgcolor, outputdate, outputreconciled, t.description, outputotheraccount, outputdeposit, outputwithdrawal, outputbalance, t.id, accountid, t.id, accountid ))

        # When the description changes, see if we have an account code
        h.add("""<script>
              $(function() {
                  var desctoaccount = %s;
                  var descs = %s;
                  $("input[name='description']").autocomplete({ source: descs }).blur(function() {
                      var oa = desctoaccount[$("input[name='description']").val()];
                      if (oa) {
                          $("select[name='otheraccount']").val(oa);
                      }
                  });
              });
              </script>""" % (json.dumps(desctoaccount), json.dumps(descs)))

        # Output form for creating a new transaction on the
        # end of the list.
        h.add("""
                <tr class=%s>
                    <td><input name="datefrom" type="hidden" value="%s"/>
                    <input name="dateto" type="hidden" value="%s"/>
                    <input id="datebox" name="date" size=10 value="%s"/></td>
                    <td><input name="reconciled" type="checkbox"/></td>
                    <td><input name="description" /></td>
                    <td><input name="account" type="hidden" value="%s"/>
                        <select name="otheraccount">%s</select></td>
                    <td class="editmoney"><input name="deposit" size=4/></td>
                    <td class="editmoney"><input name="withdrawal" size=4/></td>
                    <td><input type="submit" value="submit"></td>
                </tr>
            """ % ( editcolour, datefrom, dateto, transactions.getToday(), accountid, accounts.getAccountsAsHTML() ))
        
        # Finish up
        h.add("</form></table>")
        h.add("""
            <p><a href="index">Back</a></p>
            """)

        # Scroll to the bottom of the screen and set focus to the date
        h.add("""
        <script type="text/javascript">
        window.scrollTo(0, document.body.scrollHeight);
        $(function() {
            $("#datebox").focus();
        });
        </script>
        """)
        
        h.add(html.getHTMLFooter())
        
        return h.get()
       
class transaction_add:
    def POST(self):
        """ 
            Called when a new transaction is submitted by the UI
        """
        data = web.input(reconciled = 0, date = "", description = "", account = 0, otheraccount = 0, deposit = 0, withdrawal = 0)
            
        # Create a new transaction object from data
        t = transactions.Transaction()
        t.accountid = data.account

        # Convert user date entered to Python date for object
        datebits = data.date.split("/")
        t.date = datetime.date(int(datebits[2]), int(datebits[1]), int(datebits[0]))
    
        t.reconciled = data.reconciled
        t.description = data.description
        t.otheraccountid = data.otheraccount
        if data.deposit != "": 
            t.deposit = data.deposit
        if data.withdrawal != "":
            t.withdrawal = data.withdrawal
        
        # Submit it for saving to the db
        transactions.createTransaction(t)
        
        # Redirect back to the transaction screen
        raise web.seeother("transaction?accountid=%s&datefrom=%s&dateto=%s" % (data.account, data.datefrom, data.dateto))
        
class transaction_edit:
    def GET(self):
        """
            Screen to edit a transaction.
        """
        data = web.input(id = 0, accountid = 0)
        t = transactions.getTransactionById(data.id, data.accountid)
        outputdate = transactions.pythonToDisplayDate(t.date)
        h = html.getHTMLHeader("Edit Transaction")
        h = h + """
            <h2>Edit Transaction</h2>
            <form action="transaction_edit" method="post">
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
            """ % ( data.id, data.accountid, outputdate, t.description, accounts.getAccountsAsHTML(t.otheraccountid), t.deposit, t.withdrawal, transactions.getReconciledAsHTML(t.reconciled) )
        
        h = h + html.getHTMLFooter()    
        
        return h

    def POST(self):
        """
        Fired when the user updates an existing transaction
        """
        data = web.input(date = "", id = 0, description = "", accountid = 0, otheraccountid = 0, deposit = 0, withdrawal = 0, reconciled = 0)
        t = transactions.Transaction()
        t.id = data.id 
        t.date = transactions.displayToPythonDate(data.date)
        t.description = data.description
        t.accountid = data.accountid
        t.otheraccountid = data.otheraccountid
        t.deposit = data.deposit
        t.withdrawal = data.withdrawal
        t.reconciled = data.reconciled
        transactions.updateTransaction(t)
        raise web.seeother("transaction?accountid=%s" % data.accountid)

class transaction_reconcile:
    def GET(self):
        """
            Marks a transaction as reconciled
        """
        data = web.input(id = 0)
        transactions.markTransactionReconciled(data.id)
        raise web.seeother("transaction?accountid=%s" % (data.accountid))

class transaction_delete:
    def GET(self):
        """
            Deletes a transaction
        """
        data = web.input(id = 0)
        transactions.deleteTransaction(data.id)
        raise web.seeother("transaction?accountid=%s" % data.accountid)

class report:
    def GET(self):
        """
            CherryPy UI class for reporting functionality
        """
        h = html.StringBuilder()
        h.add(html.getHTMLHeader("Reports"))
    	h.add("<h2>Reports</h2>");
    	h.add("""
		<form action="report_render" method="post">

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
		<p><a href="index">Back</a></p>
		</form>
	      """ % (transactions.getToday(), transactions.getToday()))
       
        h.add(html.getHTMLFooter()) 
        return h.get()

class report_render:
    def POST(self):
    	"""
    	Render the given report with a from/to date
    	"""
        data = web.input(datefrom = "", dateto = "", report = "")
        # Check dates
        try:
            pyfrom = transactions.displayToPythonDate(data.datefrom)
            pyto = transactions.displayToPythonDate(data.dateto)
        except:
            return html.getHTMLHeader("Error") + "<p>Invalid date given.</p>" + html.getHTMLFooter()

        if data.report == "INCEXP":
            readabledate = data.datefrom + " - " + data.dateto
            return reports.incomeExpenditure(pyfrom, pyto, readabledate)
        if data.report == "BALSH":
            readabledate = "to " + data.dateto
            return reports.balanceSheet(pyto, readabledate)

if __name__ == "__main__":
    app.run()


