<?php

class Number{
    public $singular;
    public $singularDet;
    public $plural;
    
    public function __construct(){
    }
}

class Noun{
    public $stem;
    
    public $nominative;
    public $objective;
    public $geitive;
    public $locative;
    
    public $animate = "0";
    
    public $ruleName;
    
    public function setLocative($data){
        if(is_array($data)){
            list(
                $this->locative->singular,
                $this->locative->singularDet,
                $this->locative->plural,
                 ) = $data;
        }
    }
    
    public function setGenitive($data){
        if(is_array($data)){
            list(
                $this->geitive->singular,
                $this->geitive->singularDet,
                $this->geitive->plural,
                 ) = $data;
        }
    }
    
    public function setObjective($data){
        if(is_array($data)){
            list(
                $this->objective->singular,
                $this->objective->singularDet,
                $this->objective->plural,
                 ) = $data;
        }
    }
    
    public function setNominative($data){
        if(is_array($data)){
            list(
                $this->nominative->singular,
                $this->nominative->singularDet,
                $this->nominative->plural,
                 ) = $data;
        }
    }
    
    
    public function __construct($stem, $animate){
        $this->stem =  $stem;
        $this->animate = $animate;
        
        $this->nominative = new Number();
        $this->objective = new Number();
        $this->geitive = new Number();
        $this->locative = new Number();
        
    }
    
    public function conjugate(){
        $nounConjugatorFactory = new NounConjugatorFactory($this);
        $inflectionRule = $nounConjugatorFactory->getRule();
        $inflectionRule->conjugateAll();
    }
}
?>