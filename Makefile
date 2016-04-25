
all: compile

compile: 
	pychecker -L 300 code.py accounts.py transactions.py reports.py
	rm -f *.pyc

update:
	rsync --exclude '*.pyc' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@rawsoaa3.miniserver.com:/usr/local/lib/fb_banking/
	rsync --exclude '*.pyc' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@rawsoaa3.miniserver.com:/usr/local/lib/fb_accounts/
	rsync --exclude '*.pyc' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@rawsoaa3.miniserver.com:/usr/local/lib/fb_sole/
	ssh root@rawsoaa3.miniserver.com "/etc/init.d/fb_banking restart"
	ssh root@rawsoaa3.miniserver.com "/etc/init.d/fb_accounts restart"
	ssh root@rawsoaa3.miniserver.com "/etc/init.d/fb_sole restart"

test:
	python code.py 5000

