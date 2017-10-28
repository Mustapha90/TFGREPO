#!/bin/bash          

heroku apps:create --region eu
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set ON_HEROKU=1
heroku config:set SECRET_KEY=`openssl rand -base64 32`
git push heroku master
python manage.py makemigrations festivalapp --noinput
heroku run python manage.py makemigrations --noinput
python manage.py makemigrations auth --noinput
heroku run python manage.py migrate --noinput
heroku open

