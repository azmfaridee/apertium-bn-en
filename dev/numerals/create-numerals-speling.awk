#!/usr/bin/awk -f
BEGIN{
    FS = "\t"
}
{
    if ($2 == "e"){
        print $1"; "$1"; an;num"
        print $1"; "$1"টা; an;num"
        print $1"; "$1"টি; an;num"
        print $1"; "$1"জন; hu;num"
    }else if($2 == "n"){
        print $1"; "$1"; an;num"
    }
}

