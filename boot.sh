#!/bin/bash
cd backend
pipenv shell
while true; do
    flask db upgrade 2be4d1ae5493-1
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app