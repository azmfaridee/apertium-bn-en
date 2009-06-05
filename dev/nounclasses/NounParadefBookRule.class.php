<?php

// বই - CV
class NounParadefBookRule extends NounInflectionRule{
    
    public function __construct($noun){
        parent::__construct($noun);
        switch($this->noun->animate){
            case("0"):
                $this->ruleName = 'বই';
                break;
            case("1"):
                $this->ruleName = 'গাই';
                break;
            case("2"):
                $this->ruleName = 'ভাই';
                break;
            case("3"):
                $this->ruleName = 'সাঁই';
                break;
        }
    }
    
    public function conjugateNominative(){
        switch($this->noun->animate){
            case("0"):
                $this->noun->setNominative(array(
                    $this->noun->stem,
                    $this->noun->stem . 'টা',
                    $this->noun->stem . 'গুলো',
                                         ));
                break;
            case("1"):
                $this->noun->setNominative(array(
                    $this->noun->stem,
                    $this->noun->stem . 'টা',
                    $this->noun->stem . 'গুলো',
                                         ));
                break;
            case("2"):
                $this->noun->setNominative(array(
                    $this->noun->stem,
                    $this->noun->stem . 'টা',
                    $this->noun->stem . 'রা',
                                         ));
                break;
            case("3"):
                $this->noun->setNominative(array(
                    $this->noun->stem,
                    $this->noun->stem,
                    $this->noun->stem . 'গণ',
                                         ));
                break;
        }
    }
    public function conjugateObjective(){
        switch($this->noun->animate){
            case("0"):
                $this->noun->setObjective(array(
                    $this->noun->stem,
                    $this->noun->stem . 'টা',
                    $this->noun->stem . 'গুলো',
                                        ));
                break;
            case("1"):
                $this->noun->setObjective(array(
                    $this->noun->stem . "কে",
                    $this->noun->stem . 'টাকে',
                    $this->noun->stem . 'গুলোকে',
                                        ));
                break;
            case("2"):
                $this->noun->setObjective(array(
                    $this->noun->stem . "কে",
                    $this->noun->stem . 'টাকে',
                    $this->noun->stem . 'দেরকে',
                                        ));
                break;
            case("3"):
                $this->noun->setObjective(array(
                    $this->noun->stem . "কে",
                    $this->noun->stem . 'কে',
                    $this->noun->stem . 'গণকে',
                                        ));
                break;
        }
        
    }
    public function conjugateGenitive(){
        switch($this->noun->animate){
            case("0"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'য়ের',
                    $this->noun->stem . 'টার',
                    $this->noun->stem . 'গুলোর',
                                       ));
                break;
            case("1"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'য়ের',
                    $this->noun->stem . 'টার',
                    $this->noun->stem . 'গুলোর',
                                       ));
                break;
            case("2"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'য়ের',
                    $this->noun->stem . 'টার',
                    $this->noun->stem . 'দের',
                                       ));
                break;
            case("3"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'য়ের',
                    $this->noun->stem . 'য়ের',
                    $this->noun->stem . 'গনদের',
                                       ));
                break;
        }
        
    }
    public function conjugateLocative(){
        switch($this->noun->animate){
            case("0"):
                $this->noun->setLocative(array(
                    $this->noun->stem . 'য়ে',
                    $this->noun->stem . 'টায়',
                    $this->noun->stem . 'গুলোয়',
                                       ));
                break;
            case("1"):
                $this->noun->setLocative(array(
                    '',
                    '',
                    '',
                                       ));
                break;
            case("2"):
                $this->noun->setLocative(array(
                    '',
                    '',
                    '',
                                       ));
                break;
            case("3"):
                $this->noun->setLocative(array(
                    '',
                    '',
                    '',
                                       ));
                break;
        }
    }
    
    public function conjugateMisc(){
        
    }
}

?>
