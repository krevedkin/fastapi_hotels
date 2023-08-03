#!/bin/bash
echo hello
# Wait for the database container to be ready
# while ! nc -z test_db 5432; do
#   sleep 1
# done

# Run the Alembic migrations
# alembic upgrade head

# Execute the SQL file against the database
# psql -h test_db -U postgres -d test_db -f /code/data/initial.sql