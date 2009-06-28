<?php

// abstract class 
abstract class NounInflectionRule{
    public $noun;
    public $ruleName;
    
    public function __construct($noun){
        $this->noun = $noun;
    }
    
    public function conjugateAll(){
        $this->noun->ruleName = $this->ruleName;
        
        $this->conjugateNominative();
        $this->conjugateObjective();
        $this->conjugateGenitive();
        $this->conjugateLocative();
        
        $this->conjugateMisc();
    }
    
    public abstract function conjugateNominative();
    public abstract function conjugateObjective();
    public abstract function conjugateGenitive();
    public abstract function conjugateLocative();
    
    public abstract function conjugateMisc();
}

?>
