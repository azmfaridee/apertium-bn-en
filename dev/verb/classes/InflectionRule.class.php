<?php

// the abstract class for the inflection rule
abstract class InflectionRule{
    public $paradefName;
    
    public $verb;
    protected $negative_affix = "";
    protected $negative_affix2 = "";
    protected $negative_affix3 = "";
    
    public function __construct($verb){
        $this->verb = $verb;
        if($this->verb->negative == true){
            $this->negative_affix = "না";
            $this->negative_affix2 = "নি";
            $this->negative_affix3 = "নে";
        }
    }
    
    public abstract function conjugateInfinitive();
    public abstract function conjugateInfinitiveAlt();
    public abstract function conjugateGerund();
    
    public abstract function conjugatePresentSimple();
    public abstract function conjuagatePresentContinuous();
    
    public abstract function conjuagatePastSimple();
    public abstract function conjuagatePastContinuous();
    
    public abstract function conjuagatePastHabitual();
    public abstract function conjuagatePastConditional();
    
    
    public abstract function conjuagateFutureSimple();
    public abstract function conjuagateFutureContinuous();
    
    public abstract function conjuagatePerfect();
    public abstract function conjuagatePluPerfect();
    
    public abstract function conjuagateParticiplePast();
    public abstract function conjuagateParticipleConditional();
    
    public abstract function conjuagateImperativePresent();
    public abstract function conjuagateImperativeFuture();
    
    public abstract function conjugateMisc();
    
    public function conjugateAll(){
        $this->conjugateInfinitive();
        $this->conjugateInfinitiveAlt();
        $this->conjugateGerund();
    
        $this->conjugatePresentSimple();
        $this->conjuagatePresentContinuous();
        
        $this->conjuagatePastSimple();
        $this->conjuagatePastContinuous();
        
        $this->conjuagatePastHabitual();
        $this->conjuagatePastConditional();
        
        
        $this->conjuagateFutureSimple();
        $this->conjuagateFutureContinuous();
        
        $this->conjuagatePerfect();
        $this->conjuagatePluPerfect();
        
        $this->conjuagateParticiplePast();
        $this->conjuagateParticipleConditional();
        
        $this->conjuagateImperativePresent();
        $this->conjuagateImperativeFuture();
        
        $this->conjugateMisc();
    }
    
}

?>