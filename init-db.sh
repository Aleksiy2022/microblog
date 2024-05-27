#!/bin/bash

set -e
set -u

function create_user_and_database() {
	local database=$1
	echo "  Creating user and database '$database'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE USER $database;
	    CREATE DATABASE $database;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
	echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
	for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
		create_user_and_database $db
	done
	echo "Multiple databases created"
fi

PG_HBA_CONF="/var/lib/postgresql/data/pg_hba.conf"
if [ -f "$PG_HBA_CONF" ]; then
  echo "Modifying pg_hba.conf to use md5 for local connections"
  sed -i 's/local\s\+all\s\+all\s\+.*$/local all all md5/' "$PG_HBA_CONF"
  echo "pg_hba.conf modified"
else
  echo "pg_hba.conf not found at $PG_HBA_CONF"
fi
