<?php


// নে/দে
class ParadefTakeRule extends InflectionRule{
    public $umlaut;
    public $umlaut2;
    
    public $umlaut_negative;
    public $umlaut2_negative;    
        
    public function __construct($verb){
        parent::__construct($verb);
        
        $this->paradefName = "নে";
        
        // produce the umlaut
        $consonant = BnChars::$consonant;
        $kars = BnChars::$kars;
        
        $pattern = "/([{$consonant}])(ে)$/u";
        $replacement = "$1ি";
        $this->umlaut = preg_replace($pattern, $replacement, $this->verb->stem);
        $this->umlaut_negative = preg_replace($pattern, $replacement, $this->verb->stem_negative);
        
        $replacement = "$1া";
        $this->umlaut2 = preg_replace($pattern, $replacement, $this->verb->stem);
        $this->umlaut2_negative = preg_replace($pattern, $replacement, $this->verb->stem_negative);
    }
    
    public function conjugateInfinitive(){        
        $this->verb->setInfinitive($this->umlaut_negative . "তে");        
        
    }
    
    public function conjugateInfinitiveAlt(){
        $this->verb->setInfinitiveAlt($this->verb->stem_negative . "বার জন্য");
        
    }
    
    public function conjugateGerund(){
        $this->verb->setGerund($this->verb->stem_negative . "ওয়া");
        
    }
    
    public function conjugatePresentSimple(){
        $this->verb->setPresentSimple(array(
                                            $this->verb->stem . "ই" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ন" . $this->negative_affix,
                                            $this->umlaut2 . "ও" . $this->negative_affix,
                                            $this->umlaut . "স" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ন" . $this->negative_affix,
                                            $this->verb->stem . "য়" . $this->negative_affix,
                                            
                                            $this->verb->stem . "য়" . $this->negative_affix
                                            ));
        
    }
    public function conjuagatePresentContinuous(){
        $this->verb->setPresentContinuous(array(
                                            $this->umlaut . "চ্ছি" . $this->negative_affix,
                                            
                                            $this->umlaut . "চ্ছেন" . $this->negative_affix,
                                            $this->umlaut . "চ্ছ" . $this->negative_affix,
                                            $this->umlaut . "চ্ছিস" . $this->negative_affix,
                                            
                                            $this->umlaut . "চ্ছেন" . $this->negative_affix,
                                            $this->umlaut . "চ্ছে" . $this->negative_affix,
                                            
                                            $this->umlaut . "চ্ছে" . $this->negative_affix
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
                                            $this->umlaut . "চ্ছিলাম" . $this->negative_affix,
                                            
                                            $this->umlaut . "চ্ছিলেন" . $this->negative_affix,
                                            $this->umlaut . "চ্ছিলে" . $this->negative_affix,
                                            $this->umlaut . "চ্ছিলি" . $this->negative_affix,
                                            
                                            $this->umlaut . "চ্ছিলেন" . $this->negative_affix,
                                            $this->umlaut . "চ্ছিল" . $this->negative_affix,
                                            
                                            $this->umlaut . "চ্ছিল" . $this->negative_affix
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
                                            $this->verb->stem . "ব" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            $this->umlaut . "বি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বে" . $this->negative_affix
                                              ));
        
        
    }
    
    
    public function conjuagateFutureSimple(){
        $this->verb->setFutureSimple(array(
                                            $this->verb->stem . "ব" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            $this->umlaut . "বি" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বেন" . $this->negative_affix,
                                            $this->verb->stem . "বে" . $this->negative_affix,
                                            
                                            $this->verb->stem . "বে" . $this->negative_affix
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
                                            $this->umlaut . "য়েছি",
                                            
                                            $this->umlaut . "য়েছেন",
                                            $this->umlaut . "য়েছ",
                                            $this->umlaut . "য়েছিস",
                                            
                                            $this->umlaut . "য়েছেন",
                                            $this->umlaut . "য়েছে",
                                            
                                            $this->umlaut . "য়েছে"
                                          ));
        
        }else{
            $this->verb->setPerfect(array(
                                            $this->verb->stem . "ই" . $this->negative_affix,
                                        
                                            $this->verb->stem . "ন" . $this->negative_affix,
                                            $this->umlaut2 . "ও" . $this->negative_affix,
                                            $this->umlaut . "স" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ন" . $this->negative_affix,
                                            $this->verb->stem . "য়" . $this->negative_affix,
                                            
                                            $this->verb->stem . "য়" . $this->negative_affix
                                          ));
        
        }
        
        
        
    }
    public function conjuagatePluPerfect(){
        if($this->verb->negative == false){
            $this->verb->setPluPerfect(array(
                                            $this->umlaut . "য়েছিলাম",
                                            
                                            $this->umlaut . "য়েছিলেন",
                                            $this->umlaut . "য়েছিলে",
                                            $this->umlaut . "য়েছিলি",
                                            
                                            $this->umlaut . "য়েছিলেন",
                                            $this->umlaut . "য়েছিল",
                                            
                                            $this->umlaut . "য়েছিল"
                                             ));
        
        }else{
            $this->verb->setPluPerfect(array(
                                            $this->verb->stem . "ই" . $this->negative_affix,
                                    
                                            $this->verb->stem . "ন" . $this->negative_affix,
                                            $this->umlaut2 . "ও" . $this->negative_affix,
                                            $this->umlaut . "স" . $this->negative_affix,
                                            
                                            $this->verb->stem . "ন" . $this->negative_affix,
                                            $this->verb->stem . "য়" . $this->negative_affix,
                                            
                                            $this->verb->stem . "য়" . $this->negative_affix
                                             ));
        
        }
        
        
        
    }
    
    public function conjuagateParticiplePast(){
        $this->verb->setParticiplePast($this->umlaut_negative . "য়ে");
        
        
    }
    public function conjuagateParticipleConditional(){
        $this->verb->setParticipleConditional($this->umlaut_negative . "লে");
        
        
    }
    
    public function conjuagateImperativePresent(){
        if($this->verb->negative == false){
            $this->verb->setImperativePresent(array(
                                                    $this->verb->stem . "ন",
                                                    $this->umlaut2 . "ও",
                                                    $this->verb->stem,
                                                    
                                                    $this->verb->stem . "ন",
                                                    $this->umlaut . "ক",
                                                    $this->umlaut . "ক"
                                                    ));
            
        }else{
            $this->verb->setImperativePresent(array(
                                                    $this->verb->stem . "বেন" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix,
                                                    $this->umlaut . "বি" . $this->negative_affix,
                                                    
                                                    $this->verb->stem . "বেন" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix
                                                    ));
            
        }
    }
    
    public function conjuagateImperativeFuture(){
        $this->verb->setImperativeFuture(array(
                                                    $this->verb->stem . "বেন" . $this->negative_affix,
                                                    $this->umlaut . "ও" . $this->negative_affix,
                                                    $this->umlaut . "স" . $this->negative_affix3,
                                                    
                                                    $this->verb->stem . "বেন" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix,
                                                    $this->verb->stem . "বে" . $this->negative_affix,
                                               ));
        
    }
    
    public function conjugateMisc(){
        
    }
}

?>
