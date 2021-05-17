DB_HOST="powerdns-db"
DB_PASSWORD="pdns"
DB_USER="root"
DB_DB="pdns"

curl http://www.internic.net/domain/root.zone -o root.zone.base

awk '{if ($4=="A" || $4=="AAAA" || $4=="SOA" || $4=="NS" || $4=="DS") print $0}' root.zone.base > root.zone

echo '. 86400 IN NS pwn-machine.pwn' >> root.zone
echo 'pwn-machine.pwn. 86400 IN A 127.0.0.1' >> root.zone
mv root.zone /etc/powerdns/root.zone


while ! mysqladmin ping -h"$DB_HOST" --silent; do
    sleep 1
done

# check for db existence
echo 'SELECT 1 FROM domains;' | mysql -u "${DB_USER}" -p"${DB_PASSWORD}" -h "${DB_HOST}" "${DB_DB}"  || (
    # INIT DB
    mysql -u "${DB_USER}" -p"${DB_PASSWORD}" -h "${DB_HOST}" "${DB_DB}" < /usr/share/doc/pdns-backend-mysql/schema.mysql.sql
)
mkdir -p /var/run/pdns-recursor
# start server
poetry run python -u main.py  &
/usr/sbin/pdns_server --loglevel=9 --daemon=no &
/usr/sbin/pdns_recursor --loglevel=9 --daemon=no 
