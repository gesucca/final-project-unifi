#!/bin/sh

yes | rm -rf db
mkdir db

killall mongod
mongod --dbpath=./db
