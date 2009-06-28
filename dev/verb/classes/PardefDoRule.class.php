<?php

// কর
class PardefDoRule extends InflectionRule{

    public function __construct($verb){
        parent::__construct($verb);
        $this->paradefName = "কর";
    }
    
    
    public function conjugateInfinitive(){
        $this->verb->setInfinitive($this->verb->stem_negative . "তে");
        
    }
    
    public function conjugateInfinitiveAlt(){
        $this->verb->setInfinitiveAlt($this->verb->stem_negative . "ার জন্য");
        
    }
    
    public function conjugateGerund(){
        $this->verb->setGerund($this->verb->stem_negative . "া");
    }
    
    public function conjugatePresentSimple(){
        $this->verb->setPresentSimple(array(
                                            $this->verb->stem . "ি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "েন" . $this->negative_affix,
                                            $this->verb->stem . $this->negative_affix,
                                            $this->verb->stem . "িস" . $this->negative_affix,
                                            
                                            $this->verb->stem . "েন" . $this->negative_affix,
                                            $this->verb->stem . "ে" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ে" . $this->negative_affix
                                            ));

    }
    
    public function conjuagatePresentContinuous(){
        $this->verb->setPresentContinuous(array(
                                                $this->verb->stem . "ছি" . $this->negative_affix,
                                                
                                                $this->verb->stem . "ছেন" . $this->negative_affix,
                                                $this->verb->stem . "ছ" . $this->negative_affix,
                                                $this->verb->stem . "ছিস" . $this->negative_affix,
        
                                                $this->verb->stem . "ছেন" . $this->negative_affix,
                                                $this->verb->stem . "ছে" . $this->negative_affix,
                                                
                                                $this->verb->stem . "ছে" . $this->negative_affix
                                                ));
        
        
    }
    
    public function conjuagatePastSimple(){
        
        $this->verb->setPastSimple(array(
                                        $this->verb->stem . "লাম" . $this->negative_affix,
        
                                        $this->verb->stem . "লেন" . $this->negative_affix,
                                        $this->verb->stem . "লে" . $this->negative_affix,
                                        $this->verb->stem . "লি" . $this->negative_affix,
        
                                        $this->verb->stem . "লেন" . $this->negative_affix,
                                        $this->verb->stem . "ল" . $this->negative_affix,
        
                                        $this->verb->stem . "ল" . $this->negative_affix,
                                         ));
        
        
    }
    public function conjuagatePastContinuous(){
        $this->verb->setPastContinuous(array(
                                            $this->verb->stem . "ছিলাম" . $this->negative_affix,
        
                                            $this->verb->stem . "ছিলেন" . $this->negative_affix,
                                            $this->verb->stem . "ছিলে" . $this->negative_affix,
                                            $this->verb->stem . "ছিলি" . $this->negative_affix,
        
                                            $this->verb->stem . "ছিলেন" . $this->negative_affix,
                                            $this->verb->stem . "ছিল" . $this->negative_affix,
        
                                            $this->verb->stem . "ছিল" . $this->negative_affix,
                                             ));
        
        
    }
    
    public function conjuagatePastHabitual(){
        $this->verb->setPastHabitual(array(
                                            $this->verb->stem . "তাম" . $this->negative_affix,
                                            
                                            $this->verb->stem . "তেন" . $this->negative_affix,
                                            $this->verb->stem . "তে" . $this->negative_affix,
                                            $this->verb->stem . "তি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "তেন" . $this->negative_affix,
                                            $this->verb->stem . "ত" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ত" . $this->negative_affix
                                           ));
        
        
    }
    public function conjuagatePastConditional(){
        $this->verb->setPastConditional(array(
                                            $this->verb->stem . "ব" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            $this->verb->stem . "বি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                              ));
        
        
    }
    
    
    public function conjuagateFutureSimple(){
        $this->verb->setFutureSimple(array(
                                            $this->verb->stem . "ব" . $this->negative_affix,
        
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            $this->verb->stem . "বি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বে" . $this->negative_affix
                                           ));
        
        
    }
    
    public function conjuagateFutureContinuous(){
        $this->verb->setFutureContinuous(array(
                                                $this->verb->stem . "তে থাকব" . $this->negative_affix,
                                                
                                                $this->verb->stem . "তে থাকবেন" . $this->negative_affix,
                                                $this->verb->stem . "তে থাকবে" . $this->negative_affix,
                                                $this->verb->stem . "তে থাকবি" . $this->negative_affix,
                                                
                                                $this->verb->stem . "তে থাকবেন" . $this->negative_affix,
                                                $this->verb->stem . "তে থাকবে" . $this->negative_affix,
                                                
                                                $this->verb->stem . "তে থাকবে" . $this->negative_affix
                                               ));
        
        
        
    }
    
    public function conjuagatePerfect(){
        if($this->verb->negative == false){
            $this->verb->setPerfect(array(
                                            $this->verb->stem . "েছি",
                                            
                                            $this->verb->stem . "েছেন",
                                            $this->verb->stem . "েছ",
                                            $this->verb->stem . "েছিস",
                                            
                                            $this->verb->stem . "েছেন",
                                            $this->verb->stem . "েছে",
                                            
                                            $this->verb->stem . "েছে",
                                          ));
            
        }else{
            $this->verb->setPerfect(array(
                                            $this->verb->stem . "ি" . $this->negative_affix2,
                                            
                                            $this->verb->stem . "েন" . $this->negative_affix2,
                                            $this->verb->stem . $this->negative_affix2,
                                            $this->verb->stem . "িস" . $this->negative_affix2,
                                            
                                            $this->verb->stem . "েন" . $this->negative_affix2,
                                            $this->verb->stem . "ে" . $this->negative_affix2,
                                            
                                            $this->verb->stem . "ে" . $this->negative_affix2,
                                          ));
            
            
        }
        
    }
    public function conjuagatePluPerfect(){
        if($this->verb->negative == false){
            $this->verb->setPluPerfect(array(
                                            $this->verb->stem . "েছিলাম",
                                            
                                            $this->verb->stem . "েছিলেন",
                                            $this->verb->stem . "েছিলে",
                                            $this->verb->stem . "েছিলি",
                                            
                                            $this->verb->stem . "েছিলেন",
                                            $this->verb->stem . "েছিল",
                                            
                                            $this->verb->stem . "েছিল"
                                             ));
            
        }else{
            $this->verb->setPluPerfect(array(
                                                $this->verb->stem . "ি" . $this->negative_affix2,
                                                
                                                $this->verb->stem . "েন" . $this->negative_affix2,
                                                $this->verb->stem . $this->negative_affix2,
                                                $this->verb->stem . "িস" . $this->negative_affix2,
                                                
                                                $this->verb->stem . "েন" . $this->negative_affix2,
                                                $this->verb->stem . "ে" . $this->negative_affix2,
                                                
                                                $this->verb->stem . "ে" . $this->negative_affix2
                                             ));
            
        }
    }
    
    public function conjuagateParticiplePast(){
        $this->verb->setParticiplePast($this->verb->stem_negative . "ে");
        
        
    }
    public function conjuagateParticipleConditional(){
        $this->verb->setParticipleConditional($this->verb->stem_negative . "লে");
        
        
    }
    
    public function conjuagateImperativePresent(){
        if($this->verb->negative == false){
            $this->verb->setImperativePresent(array(
                                                    $this->verb->stem . "ুন",
                                                    $this->verb->stem,
                                                    $this->verb->stem,
                                                    $this->verb->stem . "ুন",
                                                    $this->verb->stem . "ুক",
                                                    $this->verb->stem . "ুক"
                                                    ));
            
        }else{
            $this->verb->setImperativePresent(array(
                                                    $this->verb->stem . "বেন"  . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix, 
                                                    $this->verb->stem . "বি" . $this->negative_affix,
                                                    
                                                    $this->verb->stem . "বেন"  . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix 
                                                    ));
            
        }
        
    }
    
    public function conjuagateImperativeFuture(){
        $this->verb->setImperativeFuture(array(
                                                    $this->verb->stem . "বেন" . $this->negative_affix,
                                                    $this->verb->stem . "ো" . $this->negative_affix,
                                                    $this->verb->stem . "িস" . $this->negative_affix3,
                                                    
                                                    $this->verb->stem . "বেন" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix3
                                               ));
        
    }
    
    public function conjugateMisc(){
        
    }
    
}

?>
