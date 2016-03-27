Tournament Project: this is a python module that keeps track of players and matches in a swiss game tournament

python version: 2.7.6
library needed: functools, flask, sqlalchemy, oauth2client, json

Step 1: setup and access the database:
    1.0)  cd /vagrant/tournament
    1.1)  vagrant up
    1.2)  vagrant ssh
    1.3)  cd /vagrant/tournament
	1.4)  run psql
	1.5)  \i tournmanet.sql (database created by "CREATE", and connected by "\c")
Step 2: run tournment_test.sql
    2.0) \q (exit from psql interactive mode)
    2.1) python tournament_test.py
