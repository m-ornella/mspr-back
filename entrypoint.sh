#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"

/wait-for-mysql.sh db:3306 --timeout=30 --strict -- echo "MySQL is up"

exec uvicorn app.main:app --host 0.0.0.0 --port 80
