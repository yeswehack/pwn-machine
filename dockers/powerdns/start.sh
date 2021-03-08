DB_HOST="powerdns-db"
DB_PASSWORD="pdns"
DB_USER="root"
DB_DB="pdns"
while ! mysqladmin ping -h"$DB_HOST" --silent; do
    sleep 1
done

# check for db existence
echo 'SELECT 1 FROM domains;' | mysql -u "${DB_USER}" -p"${DB_PASSWORD}" -h "${DB_HOST}" "${DB_DB}"  || (
    # INIT DB
    mysql -u "${DB_USER}" -p"${DB_PASSWORD}" -h "${DB_HOST}" "${DB_DB}" < /usr/share/doc/pdns-backend-mysql/schema.mysql.sql
)

# start server
/usr/sbin/pdns_server --loglevel=9 --daemon=no 2>&1 1>/dev/null | poetry run python -u main.py
