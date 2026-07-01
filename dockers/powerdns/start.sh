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
if [ -z "$PDNS_API_KEY" ]; then
    echo "error: \$PDNS_API_KEY missing from environment" >&2
    exit 1
fi
echo "api-key=$PDNS_API_KEY" >> /etc/powerdns/pdns.conf
echo "Starting pdns_server"
/usr/sbin/pdns_server