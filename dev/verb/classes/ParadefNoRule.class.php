<?php


// it does nothing, the factory falls back to this if it can't find any match;
class ParadefNoRule extends InflectionRule{
    
    public function __construct($verb){
        parent::__construct($verb);
        
        $this->paradefName = "none";
        //echo "No defition match for this verb<br/>";
    }
    
    public function conjugateInfinitive(){
    }
    
    public function conjugateInfinitiveAlt(){
    }
    
    public function conjugateGerund(){
    }
    
    public function conjugatePresentSimple(){
    }
    
    public function conjuagatePresentContinuous(){
    }
    
    
    public function conjuagatePastSimple(){
        
    }
    public function conjuagatePastContinuous(){
        
    }
    
    public function conjuagatePastHabitual(){
        
    }
    public function conjuagatePastConditional(){
        
    }
    
    
    public function conjuagateFutureSimple(){
        
    }
    public function conjuagateFutureContinuous(){
        
    }
    
    public function conjuagatePerfect(){
        
    }
    public function conjuagatePluPerfect(){
        
    }
    
    public function conjuagateParticiplePast(){
        
    }
    public function conjuagateParticipleConditional(){
        
    }
    
    public function conjuagateImperativePresent(){
        
    }
    public function conjuagateImperativeFuture(){
        
    }
    
    public function conjugateMisc(){
        
    }
}


?>
