#!/bin/sh

echo "DROP DATABASE if exists bengali_conjugator; CREATE DATABASE bengali_conjugator DEFAULT CHARACTER SET utf8 COLLATE utf8_bangla_ci; use bengali_conjugator;" | mysql mysql -uroot -proot

bzcat $1 | mysql bengali_conjugator -uroot -proot

echo 'Press any key to continue ...'
read dummy

