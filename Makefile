manage=./manage.py
python=python3

runserver:
	$(python) $(manage) runserver


migrate:
	$(python) $(manage) makemigrations 
	$(python) $(manage) migrate


superuser:
	$(python) $(manage)

superadmin:
	$(python) $(manage) createsuperadmin

role:
	$(python) $(manage) createrole

shell:
	$(python) $(manage) shell_plus

set-up:
	$(python) $(manage) createrole 
	$(python) $(manage) createsuperadmin 

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

test-user:
	$(python) $(manage) test user.tests 
test-school:
	$(python) $(manage) test school.tests 

	
