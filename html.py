#!/usr/bin/env python

version = "v20161221"
copyyear = "2005-2016"

def getHTMLHeader(title):
    """
        The HTML header for all pages
    """
    return """
            <html>
            <head>
            <title>FruityBanking - %s</title>
            <link rel="stylesheet" href="static/style.css" />
            <link type="text/css" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet" />
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
            <script type="text/javascript" src="static/fb.js"></script>
            </head>
            <body>            
	    <img src="static/fruity.png" align="right" />
       """ % title
       
def getHTMLFooter():
    """
        The HTML footer for all pages
    """
    return """
            <div id="footer"><span class="brand">FB! %s</span><br/><span class="copyright">
               Copyright(c)%s, R. Rawson-Tetley. This software is covered
               under the terms of the 
               <a href="http://www.gnu.org/copyleft/gpl.html">GNU General Public License.</a>
               </span></div>
            </body></html>
        """ % ( version, copyyear )

from cStringIO import StringIO

class StringBuilder:
	def __init__(self):
		self.buffer = StringIO()
	def add(self, s):
		if isinstance(s, unicode):
			s = s.encode("ascii", "xmlcharrefreplace")
		self.buffer.write(s)
	def get(self):
		return self.buffer.getvalue()

