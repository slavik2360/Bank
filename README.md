# django_rest
Django REST

# How to deploy ?

## Install requirements
#MacOs or Linux
pip install -r tools/requirements/base.txt
pip install psycopg2-binary
#Windows
pip install -r tools\requirements\base.txt
pip install psycopg2

## Apply migrations

python manage.py migrate

## Create superuser

python manage.py users

## Runserver

python manage.py runserver
