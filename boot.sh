#!/bin/bash
source venv/bin/activate
while true; do
    flask db upgrade 05fce74b56cb
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask db upgrade 2be4d1ae5493
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app