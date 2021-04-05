
setup:
	pip install pwn-machine

build:
	echo "building"

run:
	pm setup

dockertest:
	make setup
	make build
	make run

