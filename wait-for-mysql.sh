#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until mysqladmin ping -h "$host" -u root -p"${MYSQL_ROOT_PASSWORD}" &>/dev/null; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd
