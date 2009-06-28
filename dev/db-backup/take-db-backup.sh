#!/bin/sh

mysqldump -uroot -proot --routines bengali_conjugator | bzip2 > bengali_conjugator$(date +_%Y%m%d_%H%M).sql.bz2
