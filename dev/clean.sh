#!/bin/sh

folders=$(find -name '*~')
echo "REMOVING: $folders"
if [ "$folders" != "" ]
    then rm -rf $folders
fi

