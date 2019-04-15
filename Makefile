
all: compile

compile: 
	pychecker -L 300 code.py accounts.py transactions.py reports.py
	rm -f *.pyc

update:
	#rsync --exclude '*.pyc' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@rawsoaa3.miniserver.com:/usr/local/lib/fb_banking/
	#rsync --exclude '*.pyc' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@rawsoaa3.miniserver.com:/usr/local/lib/fb_sole/
	rsync --exclude '*.pyc' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@servicedx.sheltermanager.com:/usr/local/lib/fb_accounts/
	#ssh root@rawsoaa3.miniserver.com "touch /usr/local/lib/fb_banking/code.py && touch /usr/local/lib/fb_sole/code.py"
	ssh root@servicedx.sheltermanager.com "touch /usr/local/lib/fb_accounts/code.py"

test:
	python code.py 5000

