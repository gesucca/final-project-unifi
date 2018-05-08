#!/bin/sh

# extract fields list from big collection and reset dataset directory
# actual export command has been moved to makefile

mongo < list_attr.mongosh > _exp_fields.txt
sed -i -e 's/	"//g' _exp_fields.txt
sed -i -e 's/"//g' _exp_fields.txt
sed -i -e 's/,//g' _exp_fields.txt
sed -i -e '1,16d' _exp_fields.txt # mongo client echoed stuff
sed -i -e 's/_id//g' _exp_fields.txt
sed -i -e 's/bye//g' _exp_fields.txt
sed -i -e '/^\s*$/d' _exp_fields.txt # empty lines

cd ..
yes | rm -rf datasets
mkdir datasets
