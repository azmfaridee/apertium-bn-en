#!/bin/sh

folders=$(find -name '*~')
echo "REMOVING: $folders"
if [ "$folders" != "" ]
    then rm -rf $folders
fi
echo 'Press any key to continue ....'
read dummy

