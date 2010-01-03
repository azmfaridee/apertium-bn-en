#!/bin/sh

echo "DROP DATABASE if exists bengali_conjugator; CREATE DATABASE bengali_conjugator DEFAULT CHARACTER SET utf8 COLLATE utf8_bangla_ci; use bengali_conjugator;" | mysql mysql -uroot -proot

# we are not using bzipped tar files for backup anymore
# bzcat $1 | mysql bengali_conjugator -uroot -proot
cat mysqldump.sql | mysql bengali_conjugator -uroot -proot

echo 'Press any key to continue ...'
read dummy

