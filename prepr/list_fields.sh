#!/bin/sh

mongo < list_attr.mongosh > _exp_fields.txt
sed -i -e 's/	//g' _exp_fields.txt
sed -i -e 's/,\n//g' _exp_fields.txt
sed -i -e '1,16d' _exp_fields.txt # mongo client echoed stuff
sed -i -e 's/_id//g' _exp_fields.txt
sed -i -e 's/bye//g' _exp_fields.txt
sed -i -e '/^\s*$/d' _exp_fields.txt # empty lines

echo "CLEAN IT UP MANUALLY, CAN'T BOTHER TO MAKE IT WORK AUTOMATICALLY"
