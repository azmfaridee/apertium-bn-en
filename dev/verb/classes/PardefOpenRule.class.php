<?php

// খোল/দোল
class PardefOpenRule extends InflectionRule{
    public $umlaut;
    public $umlaut_negative;

    public function __construct($verb){
        parent::__construct($verb);
        
        $this->paradefName = "খোল";
        
        // produce the umlaut
        $consonant = BnChars::$consonant;
        $kars = BnChars::$kars;
        
        $pattern = "/(ো)(ঁ?)([{$consonant}])$/u";
        $replacement = "ু$2$3";
        $this->umlaut = preg_replace($pattern, $replacement, $this->verb->stem);
        $this->umlaut_negative = preg_replace($pattern, $replacement, $this->verb->stem_negative);
    }
    
    
    public function conjugateInfinitive(){
        $this->verb->setInfinitive($this->umlaut_negative . "তে");
        
    }
    
    public function conjugateInfinitiveAlt(){
        $this->verb->setInfinitiveAlt($this->verb->stem_negative . "ার জন্য");
        
    }
    
    public function conjugateGerund(){
        $this->verb->setGerund($this->verb->stem_negative . "া");
        
    }
    
    public function conjugatePresentSimple(){
        $this->verb->setPresentSimple(array(
                                            $this->umlaut . "ি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "েন" . $this->negative_affix,
                                            $this->verb->stem . $this->negative_affix,
                                            $this->umlaut . "িস" . $this->negative_affix,
                                            
                                            $this->verb->stem . "েন" . $this->negative_affix,
                                            $this->verb->stem . "ে" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ে" . $this->negative_affix
                                            ));
        
    }
    public function conjuagatePresentContinuous(){
        
        $this->verb->setPresentContinuous(array(
                                                $this->umlaut . "ছি" . $this->negative_affix,
                                                
                                                $this->umlaut . "ছেন" . $this->negative_affix,
                                                $this->umlaut . "ছ" . $this->negative_affix,
                                                $this->umlaut . "ছিস" . $this->negative_affix,
                                                
                                                $this->umlaut . "ছেন" . $this->negative_affix,
                                                $this->umlaut . "ছে" . $this->negative_affix,
                                                
                                                $this->umlaut . "ছে" . $this->negative_affix
                                                ));
        
    }
    
    public function conjuagatePastSimple(){
        $this->verb->setPastSimple(array(
                                        $this->umlaut . "লাম" . $this->negative_affix,
                                        
                                        $this->umlaut . "লেন" . $this->negative_affix,
                                        $this->umlaut . "লে" . $this->negative_affix,
                                        $this->umlaut . "লি" . $this->negative_affix,
                                        
                                        $this->umlaut . "লেন" . $this->negative_affix,
                                        $this->umlaut . "ল" . $this->negative_affix,
                                        
                                        $this->umlaut . "ল" . $this->negative_affix
                                         ));
        
        
        
    }
    public function conjuagatePastContinuous(){
        $this->verb->setPastContinuous(array(
                                                $this->umlaut . "ছিলাম" . $this->negative_affix,
                                                
                                                $this->umlaut . "ছিলেন" . $this->negative_affix,
                                                $this->umlaut . "ছিলে" . $this->negative_affix,
                                                $this->umlaut . "ছিলি" . $this->negative_affix,
                                                
                                                $this->umlaut . "ছিলেন" . $this->negative_affix,
                                                $this->umlaut . "ছিল" . $this->negative_affix,
                                                
                                                $this->umlaut . "ছিল" . $this->negative_affix
                                             ));
                
    }
    
    public function conjuagatePastHabitual(){
        $this->verb->setPastHabitual(array(
                                            $this->umlaut . "তাম" . $this->negative_affix,
                                            
                                            $this->umlaut . "তেন" . $this->negative_affix,
                                            $this->umlaut . "তে" . $this->negative_affix,
                                            $this->umlaut . "তি" . $this->negative_affix,
                                            
                                            $this->umlaut . "তেন" . $this->negative_affix,
                                            $this->umlaut . "ত" . $this->negative_affix,
                                            
                                            $this->umlaut . "ত" . $this->negative_affix
                                           ));
        
        
    }
    public function conjuagatePastConditional(){
        $this->verb->setPastConditional(array(
                                                $this->umlaut . "ব" . $this->negative_affix,
                                                
                                                $this->umlaut . "বেন" . $this->negative_affix,
                                                $this->umlaut . "বে" . $this->negative_affix,
                                                $this->umlaut . "বি" . $this->negative_affix,
                                                
                                                $this->umlaut . "বেন" . $this->negative_affix,
                                                $this->umlaut . "বে" . $this->negative_affix,
                                                
                                                $this->umlaut . "বে" . $this->negative_affix
                                              ));
        
        
    }
    
    
    public function conjuagateFutureSimple(){
        $this->verb->setFutureSimple(array(
                                            $this->umlaut . "ব" . $this->negative_affix,
                                            
                                            $this->umlaut . "বেন" . $this->negative_affix,
                                            $this->umlaut . "বে" . $this->negative_affix,
                                            $this->umlaut . "বি" . $this->negative_affix,
                                            
                                            $this->umlaut . "বেন" . $this->negative_affix,
                                            $this->umlaut . "বে" . $this->negative_affix,
                                            
                                            $this->umlaut . "বে" . $this->negative_affix
                                           ));
        
    }
    
    public function conjuagateFutureContinuous(){
        $this->verb->setFutureContinuous(array(
                                                $this->umlaut . "তে থাকব" . $this->negative_affix,
                                                
                                                $this->umlaut . "তে থাকবেন" . $this->negative_affix,
                                                $this->umlaut . "তে থাকবে" . $this->negative_affix,
                                                $this->umlaut . "তে থাকবি" . $this->negative_affix,
                                                
                                                $this->umlaut . "তে থাকবেন" . $this->negative_affix,
                                                $this->umlaut . "তে থাকবে" . $this->negative_affix,
                                                
                                                $this->umlaut . "তে থাকবে" . $this->negative_affix
                                               ));
        
        
    }
    
    public function conjuagatePerfect(){
        if($this->verb->negative == false){
            $this->verb->setPerfect(array(
                                            $this->umlaut . "েছি",
                                        
                                            $this->umlaut . "েছেন",
                                            $this->umlaut . "েছ",
                                            $this->umlaut . "েছিস",
                                            
                                            $this->umlaut . "েছেন",
                                            $this->umlaut . "েছে",
                                            
                                            $this->umlaut . "েছে"
                                          ));
            
        }
        else{
            $this->verb->setPerfect(array(
                                            $this->umlaut . "ি" . $this->negative_affix2,
                                        
                                            $this->umlaut . "েন" . $this->negative_affix2,
                                            $this->umlaut . $this->negative_affix2,
                                            $this->umlaut . "িস" . $this->negative_affix2,
                                            
                                            $this->umlaut . "েন" . $this->negative_affix2,
                                            $this->umlaut . "ে" . $this->negative_affix2,
                                            
                                            $this->umlaut . "ে" . $this->negative_affix2
                                          ));
            
            
        }
        
        
    }
    public function conjuagatePluPerfect(){
        if($this->verb->negative == false){
            $this->verb->setPluPerfect(array(
                                            $this->umlaut . "েছিলাম",
                                        
                                            $this->umlaut . "েছিলেন",
                                            $this->umlaut . "েছিলে",
                                            $this->umlaut . "েছিলি",
                                            
                                            $this->umlaut . "েছিলেন",
                                            $this->umlaut . "েছিল",
                                            $this->umlaut . "েছিল",
                                            
                                            $this->umlaut . "েছিল"
                                          ));
            
        }
        else{
            $this->verb->setPluPerfect(array(
                                            $this->umlaut . "ি" . $this->negative_affix2,
                                        
                                            $this->umlaut . "েন" . $this->negative_affix2,
                                            $this->umlaut . $this->negative_affix2,
                                            $this->umlaut . "িস" . $this->negative_affix2,
                                            
                                            $this->umlaut . "েন" . $this->negative_affix2,
                                            $this->umlaut . "ে" . $this->negative_affix2,
                                            
                                            $this->umlaut . "ে" . $this->negative_affix2
                                          ));
            
        }                
        
    }
    
    public function conjuagateParticiplePast(){
        $this->verb->setParticiplePast($this->umlaut_negative . "ে");
        
    }
    public function conjuagateParticipleConditional(){
        $this->verb->setParticipleConditional($this->umlaut_negative . "লে");
        
    }
    
    public function conjuagateImperativePresent(){
        if($this->verb->negative == false){
            $this->verb->setImperativePresent(array(
                                                    $this->umlaut . "ুন",
                                                    $this->verb->stem,
                                                    $this->umlaut,
                                                    
                                                    $this->umlaut . "ুন",
                                                    $this->umlaut . "ুক",
                                                    $this->umlaut . "ুক"
                                                    ));
        
        }else{
            $this->verb->setImperativePresent(array(
                                                    $this->umlaut . "বেন" . $this->negative_affix,
                                                    $this->umlaut . "বে" . $this->negative_affix,
                                                    $this->umlaut . "বি" . $this->negative_affix,
                                                    
                                                    $this->umlaut . "বেন" . $this->negative_affix,
                                                    $this->umlaut . "বে" . $this->negative_affix,
                                                    $this->umlaut . "বে" . $this->negative_affix
                                                    ));
            
        }
    }
    
    public function conjuagateImperativeFuture(){
        $this->verb->setImperativeFuture(array(
                                                    $this->umlaut . "বেন" . $this->negative_affix,
                                                    $this->verb->stem . "ো" . $this->negative_affix,
                                                    $this->umlaut . "িস" . $this->negative_affix3,
                                                    
                                                    $this->umlaut . "বেন" . $this->negative_affix,
                                                    $this->umlaut . "বে" . $this->negative_affix,
                                                    $this->umlaut . "বে" . $this->negative_affix
                                               ));
        
    }
        
    public function conjugateMisc(){
        
    }
    
}


?>
