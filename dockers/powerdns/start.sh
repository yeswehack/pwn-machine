while ! mysqladmin ping -h"$MYSQL_HOST" --silent; do
    sleep 1
done

# check for db existence
echo 'SELECT 1 FROM domains;' | mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -h "${MYSQL_HOST}" "${MYSQL_DATABASE}"  || (
    # INIT DB
    mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -h "${MYSQL_HOST}" "${MYSQL_DATABASE}" < /usr/share/doc/pdns-backend-mysql/schema.mysql.sql
)
# start syslog
chown -R syslog /logs/pdns
rsyslogd
# start server
echo "Starting pdns_server"
/usr/sbin/pdns_server