#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"


exec uvicorn app.main:app --host 0.0.0.0 --port 80
