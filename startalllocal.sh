#!/bin/zsh
cd "$(dirname "$0")"

terminator --new-tab -e 'docker-compose up' -T 'docker-compose' &
terminator --new-tab -e 'cd pm-manager/back; FLASK_DEBUG=1 ./venv/bin/flask run' -T 'Flask' &
terminator --new-tab -e 'cd pm-manager/quasar; quasar dev' -T 'Quasar'&
terminator --new-tab -e 'pm ssh -- -L 4242:192.168.160.3:8081 -L 4243:172.24.0.4:8080' -T 'SSH tunnel' &
