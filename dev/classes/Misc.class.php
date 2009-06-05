<?php


// this class holds the bengali vowel and consonant table
class BnChars{
    //অআইঈউঊঋএঐওঔািুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঁংঃ্
    
    public static $vowel = "অআইঈউঊঋএঐওঔ";
    public static $kars = "ািীুূৃেৈোৌ";
    public static $consonant = "কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঁ";
    public static $misc = "ংঃ্";
    public static $alphabet = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঁংঃ্";
}


// convert multibyte string to array
function mbStringToArray ($string) {
    $strlen = mb_strlen($string);
    while ($strlen) {
        $array[] = mb_substr($string,0,1,"UTF-8");
        $string = mb_substr($string,1,$strlen,"UTF-8");
        $strlen = mb_strlen($string);
    }
    return $array;
}

// convert arrry to multibyte string
function arrayTombString($array){
    return implode('', $array);
}


// TODO: this class will generatate the appropirate posfix class for our verb
class PostFixFactory{
    public function __construct(){
        
    }
}

// TODO: this class will hold the static constants for the postfix
class PostFix{
    
}

?>
