<?php

class NounConjugatorFactory{
    public $noun;
    
    public function __construct($noun){
        try{
            if($noun instanceof Noun){
                $this->noun = $noun;
            }    
        }catch(Exception $e){
            die($e->getMessage());
        }
    }
    
    public function getRule(){
        $subject = $this->noun->stem;
        
        $consonant = BnChars::$consonant;
        $vowel = BnChars::$vowel;
        $misc = BnChars::$misc;
        $kars = BnChars::$kars;
        
        // বই
        $pattern = "/([{$vowel}])(ঁ?)$/u";
        if(preg_match($pattern, $subject)){
            //echo "Book";
            return new NounParadefBookRule($this->noun);
        }
        
        // কলম
        $pattern = "/([{$consonant}])(ঁ?)$/u";
        if(preg_match($pattern, $subject)){
            //echo "Pen";
            return new NounParadefPenRule($this->noun);
        }
        
        // চাবি
        $pattern = "/([{$kars}](ঁ?))$/u";
        if(preg_match($pattern, $subject)){
            //echo "Key";
            return new NounParadefKeyRule($this->noun);
        }
        
        return new NounParadefNoRule($this->noun);
        
    }
    
}

?>
