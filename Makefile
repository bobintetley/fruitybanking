
all: compile

compile: 
	flake8 --config flake8.conf src/*.py

update:
	rsync --exclude '*.pyc' --exclude '__pycache__' --exclude 'sitedefs.py' --exclude 'fruitybanking.db' -r * root@servicedx.sheltermanager.com:/usr/local/lib/fb_accounts/
	ssh root@servicedx.sheltermanager.com "touch /usr/local/lib/fb_accounts/code.py"

test:
	python3 code.py 5010

