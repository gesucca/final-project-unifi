#!/bin/sh

yes | rm -rf db
mkdir db

# dunno who launch it and for what
sudo killall mongod

mongod --dbpath=./db
