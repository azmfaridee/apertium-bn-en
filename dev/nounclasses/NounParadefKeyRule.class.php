<?php

// চাবি - CK
class NounParadefKeyRule extends NounInflectionRule{
    
    public function __construct($noun){
        parent::__construct($noun);
        switch($this->noun->animate){
            case("0"):
                $this->ruleName = 'চাবি';
                break;
            case("1"):
                $this->ruleName = 'গাভী';
                break;
            case("2"):
                $this->ruleName = 'ভাবি';
                break;
            case("3"):
                $this->ruleName = 'কবি';
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
                    $this->noun->stem . 'র',
                    $this->noun->stem . 'টার',
                    $this->noun->stem . 'গুলোর',
                                       ));
                break;
            case("1"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'র',
                    $this->noun->stem . 'টার',
                    $this->noun->stem . 'গুলোর',
                                       ));
                break;
            case("2"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'র',
                    $this->noun->stem . 'টার',
                    $this->noun->stem . 'দের',
                                       ));
                break;
            case("3"):
                $this->noun->setGenitive(array(
                    $this->noun->stem . 'র',
                    $this->noun->stem . 'র',
                    $this->noun->stem . 'গনদের',
                                       ));
                break;
        }
        
    }
    public function conjugateLocative(){
        switch($this->noun->animate){
            case("0"):
                $this->noun->setLocative(array(
                    $this->noun->stem . 'তে',
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
