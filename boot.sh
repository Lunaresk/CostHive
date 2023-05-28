#!/bin/bash
echo "Activating venv"
source venv/bin/activate
cd backend
echo "Upgrading database"
for i in {0..5}
do
    flask db upgrade 2be4d1ae5493-1
    if [[ "$?" == "0" ]]; then
        break
    elif [ "$i" -eq 5 ]; then
        echo Deployment failed, exiting...
        exit 1
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app