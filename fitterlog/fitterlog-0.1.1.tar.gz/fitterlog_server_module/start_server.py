import os
import sys

def run():
	os.chdir(os.path.dirname(__file__))
	sys.path.append(os.path.abspath("."))
	
	if os.system("python manage.py migrate") > 0:
		os.system("python3 manage.py migrate")

	if os.system("python manage.py runserver") > 0:
		os.system("python3 manage.py runserver")