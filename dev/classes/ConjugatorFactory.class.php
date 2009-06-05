<?php

// this class chooses the appropriate conjugator rules based on the verb
class ConjugatorFactory{
    public $verb;
    
    public function __construct($verb){
            $this->verb = $verb;
    }
    
    public function getRule(){
        $subject = $this->verb->stem;
        
        $consonant = BnChars::$consonant;
        $vowel = BnChars::$vowel;
        $misc = BnChars::$misc;
        $kars = BnChars::$kars;
        
        // remember, the ordering here is very important ...
        
        // CCK/KCK করা/পড়া/নাড়া
        $pattern = "/(([{$consonant}]{2})|([{$kars}|{$vowel}][{$consonant}]))[{$kars}]{1}$/u";
        if(preg_match($pattern, $subject)){
            //echo "Make";
            return new ParadefMakeDoRule($this->verb);
        }
        
        // CKC/CKঁC খোল
        $pattern = "/(ো)(ঁ?)([{$consonant}])$/u";
        if(preg_match($pattern, $subject)){
            //echo "Open";
            return new PardefOpenRule($this->verb);
        }
        
        // CKC/CKঁC কাট/হাঁট/আঁক
        $pattern = "/[{$kars}|আ](ঁ?)[{$consonant}]$/u";
        if(preg_match($pattern, $subject)){
            //echo "Shake";
            return new PardefShakeRule($this->verb);
        }
        
        // CC/VC কর/উঠ
        $pattern = "/([{$consonant}]|[{$vowel}])([{$consonant}])$/u";
        if(preg_match($pattern, $subject)){
            //echo "Do";
            return new PardefDoRule($this->verb);
        }
        
        
        // CK যা 
        $pattern = "/(যা)$/u";
        if(preg_match($pattern, $subject)){
            //echo "Go";
            return new ParadefGoRule($this->verb);
        }
        
        // CK নে/দে
        $pattern = "/[{$consonant}](ে)$/u";
        if(preg_match($pattern, $subject)){
            //echo "Take";
            return new ParadefTakeRule($this->verb);
        }
        
        // CK খা/পা
        $pattern = "/[{$consonant}][{$kars}]$/u";
        if(preg_match($pattern, $subject)){
            //echo "Eat";
            return new ParadefEatRule($this->verb);
        }
        
        // C ক/হ
        $pattern = "/[{$consonant}]$/u";
        if(preg_match($pattern, $subject)){
            //echo "Say";
            return new ParadefEatRule($this->verb); // this might break in the future, be careful
        }
        
        return new ParadefNoRule($this->verb);
        
    }
    
}

?>
