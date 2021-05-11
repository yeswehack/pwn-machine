#!/bin/zsh
cd "$(dirname "$0")"

terminator --new-tab -e 'docker-compose up;$SHELL' -T 'DOCKER' &
terminator --new-tab -e 'cd dockers/manager/back; PM_DISABLE_AUTH=1 poetry run uvicorn app:app --port 8000 --debug;$SHELL' -T 'BACK' &
terminator --new-tab -e 'cd dockers/manager/front; yarn dev;$SHELL' -T 'FRONT' &
