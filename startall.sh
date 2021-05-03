#!/bin/zsh
cd "$(dirname "$0")"

terminator --new-tab -e 'docker-compose up' -T 'docker-compose' &
terminator --new-tab -e 'cd dockers/manager/back; poetry run uvicorn app:app --port 8000 --debug' -T 'Flask' &
terminator --new-tab -e 'cd dockers/manager/front; yarn dev' -T 'Flask' &
