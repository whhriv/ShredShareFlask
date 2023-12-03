# ShredShare Flask backend.

## Overview

This is a backend RESTAPI Built with Flask and used sqlAlchemy as the ORM. Database hosted by elephantSQL

## Installation OSX:
Clone my git Repo
```
git clone https://github.com/whhriv/ShredShareFlask .
```
Set Up python virtual environments
```
python3 -m venv venv
```
Activating the virtual env
```
. venv/bin/activate
```
Installing Requirements for the project
```
pip install -r requirements.txt
```
Create the db in flask shell and do migrations
```
  flask db init
  flask db migrate -m "initial migration"
  flask db upgrade
```
Initializing THe db if you are using a different URI
```
  flask shell
  db.create_all()
```
To run backend locally:
```
flask run --debug
```