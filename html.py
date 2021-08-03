
version = "v20210803"
copyyear = "2005-2021"

from sitedefs import SHOW_VAT

def getHTMLHeader(title):
    """
        The HTML header for all pages
    """
    return """<!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8" />
            <title>FruityBanking - %s</title>
            <link rel="stylesheet" href="static/style.css" />
            <link type="text/css" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet" />
            <script type="text/javascript">
            SHOW_VAT = %s;
            </script>
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
            <script type="text/javascript" src="static/fb.js"></script>
            </head>
            <body>            
	    <img src="static/fruity.png" align="right" />
       """ % (title, SHOW_VAT and "true" or "false")
       
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

class StringBuilder:
    buffer = [] 
    def __init__(self):
        self.buffer = []
    def add(self, s):
        self.buffer.append(s)
    def get(self):
        return "".join(self.buffer)

