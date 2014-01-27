#!/usr/bin/env python

import accounts
import html

def flt(x):
	if x == None: return float(0)
	if str(x) == "": return float(0)
	return float(x)

def balanceSheet(dateto, readabledate):
    """ 
    Prepares a balance sheet upto the date given
    and returns it as HTML
    """
    h = html.StringBuilder()
    h.add(html.getHTMLHeader("Balance Sheet"))
    h.add("<h1>Balance Sheet (%s)</h1>" % readabledate)

    # Assets
    h.add("<table width=\"75%\"><tr><td>")
    h.add("<h2>Assets</h2>")
    h.add("<table><tr>")
    assets = flt(0)
    liabilities = flt(0)

    # Cash
    h.add("<td>Cash</td><td>")

    l = accounts.totalBalanceForPeriod(dateto, 0)
    ct = flt(0)
    for i in l:
        ct += flt(i[1])

    h.add("%0.2f</td></tr>" % ct)
    assets += ct

    # Pensions
    h.add("<tr><td>Pensions</td><td>")

    l = accounts.totalBalanceForPeriod(dateto, 5)
    ct = flt(0)
    for i in l:
        ct += flt(i[1])

    h.add("%0.2f</td></tr>" % ct)
    assets += ct

    # Shares
    h.add("<tr><td>Shares</td><td>")

    l = accounts.totalBalanceForPeriod(dateto, 6)
    ct = flt(0)
    for i in l:
        ct += flt(i[1])

    h.add("%0.2f</td></tr>" % ct)
    assets += ct

    # Other Assets
    l = accounts.totalBalanceForPeriod(dateto, 10)
    for i in l:
        h.add("""
            <tr>
                <td>%s</td>
                <td>%0.2f</td>
            </tr>
              """ % ( i[0], i[1] ))
    assets += flt(i[1])

    # Liabilities
    h.add("</tr></table></td><td>")
    h.add("<h2>Liabilities</h2>")
    h.add("<table><tr>")

    # Loans
    l = accounts.totalBalanceForPeriod(dateto, 2)
    for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], abs(i[1]) ))
                liabilities += abs(flt(i[1]))

    # Credit Cards
    l = accounts.totalBalanceForPeriod(dateto, 1)
    for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], abs(i[1]) ))
                liabilities += flt(abs(i[1]))

    # Liabilities
    l = accounts.totalBalanceForPeriod(dateto, 11)
    for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], abs(i[1]) ))
                liabilities += flt(abs(i[1]))

    h.add("</table>")

    # Asset total
    h.add("</td><tr></tr><tr>")
    h.add("<td align='right'><b>%0.2f</b></td>" % assets)

    # Liabilities total
    h.add("<td align='right'><b>%0.2f</b></td>" % liabilities)
    h.add("</tr></table>")

    # Net worth
    h.add("<h3>Net worth: %0.2f</h3>" % flt(assets - liabilities))

    h.add(html.getHTMLFooter())
    return h.get()

def incomeExpenditure(datefrom, dateto, readabledate):
	"""
		Prepares an income and expenditure report for the
		two dates given and returns it as HTML.
	"""

	h = html.StringBuilder()
	h.add(html.getHTMLHeader("Income and Expenditure Report"))
        h.add("<h1>Income and Expenditure Report (%s)</h1>" % readabledate)

	# Expenses first (only deposits)
	h.add("<h2>Expenses</h2>")
	l = accounts.totalForPeriod(datefrom, dateto, 3, True)
	h.add("<table>")
	et = flt(0)
	for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], flt(i[1]) ))
		et = et + flt(i[1])
	h.add("<tr><td><b>Total</b></td><td><b>%0.2f</b></td></tr>" % flt(et))
	h.add("</table>")

	# Loan payments (only deposits)
	h.add("<h2>Loan Payments</h2>")
	l = accounts.totalForPeriod(datefrom, dateto, 2, True)
	h.add("<table>")
	lt = flt(0)
	for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], i[1] ))
		lt = lt + flt(i[1])
	h.add("<tr><td><b>Total</b></td><td><b>%0.2f</b></td></tr>" % flt(lt))
	h.add("</table>")

	# Credit card payments (only deposits)
	h.add("<h2>Credit Card Payments</h2>")
	l = accounts.totalForPeriod(datefrom, dateto, 1, True)
	h.add("<table>")
	ct = flt(0)
	for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], i[1] ))
		ct = ct + flt(i[1])
	h.add("<tr><td><b>Total</b></td><td><b>%0.2f</b></td></tr>" % flt(ct))
	h.add("</table>")

	# Total expenditure
	h.add("<h3>Total expenditure: %0.2f</h3>" % flt(ct + lt + et))

	# Income (only withdrawals)
	h.add("<h2>Income</h2>")
	l = accounts.totalForPeriod(datefrom, dateto, 4, False)
	h.add("<table>")
	ti = flt(0)
	for i in l:
		h.add("""
			<tr>
				<td>%s</td>
				<td>%0.2f</td>
			</tr>
		      """ % ( i[0], flt(i[1]) ))
		ti = ti + flt(i[1])
	h.add("<tr><td><b>Total</b></td><td><b>%0.2f</b></td></tr>" % flt(ti))
	h.add("</table>")

	# Total income
	h.add("<h3>Total income: %0.2f</h3>" % flt(ti))

	h.add(html.getHTMLFooter())
	return h.get()


