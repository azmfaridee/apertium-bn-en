<?php
/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * Description of Verb
 *
 * @author zaher
 */

require_once 'classes/InflectionRule.class.php';

require_once 'classes/ParadefNoRule.class.php';

require_once 'classes/ParadefEatRule.class.php';
require_once 'classes/ParadefTakeRule.class.php';
require_once 'classes/PardefDoRule.class.php';
require_once 'classes/PardefOpenRule.class.php';
require_once 'classes/ParadefGoRule.class.php';
require_once 'classes/PardefShakeRule.class.php';
require_once 'classes/ParadefMakeDoRule.class.php';

require_once 'classes/ConjugatorFactory.class.php';

require_once 'classes/Misc.class.php';


// honorifics for sencond person
class Honorifics2nd{
    public $informal;
    public $semiInformal;
    public $formal;
}

// honorifics for third person
class Honorifics3rd{
    public $informal;
    public $formal;

}

// person
class Person{
    
    public $firstPerson;
    public $secondPerson;
    public $thirdPerson;
    public $impersonal;

    public function __construct() {
        
        $this->secondPerson = new Honorifics2nd();
        $this->thirdPerson = new Honorifics3rd();
        
        
    }
    
}

// our main class the hold the data of the verb being conjugated
class Verb {
    public $stem;       // string
    public $negative;   // true/false
    public $stem_negative;

    public $infinitive;
    public $infinitiveAlt;
    public $gerund;

    public $presentSimple;
    public $presentContinuous;
    
    public $pastSimple;
    public $pastContinuous;
    public $pastHabitual;
    public $pastConditional;

    public $futureSimple;
    public $futureContinuous;

    public $perfect;
    public $pluPerfect;

    public $participlePast;
    public $participleConditional;

    public $imperativePresent;
    public $imperativeFuture;
    
    public $paradefName;
    
    public function setInfinitive($data){
        $this->infinitive = $data;
    }
    public function setInfinitiveAlt($data){
        $this->infinitiveAlt = $data;
    }
    public function setGerund($data){
        $this->gerund = $data;
    }
    
    public function setPresentSimple($data){
        if(is_array($data)){
            list(
                 $this->presentSimple->firstPerson,
                 
                 $this->presentSimple->secondPerson->formal,
                 $this->presentSimple->secondPerson->semiInformal,
                 $this->presentSimple->secondPerson->informal,
                 
                 $this->presentSimple->thirdPerson->formal,
                 $this->presentSimple->thirdPerson->informal,
                 
                 $this->presentSimple->impersonal
                 ) = $data;
        }
    }
    
    public function setPresentContinuous($data){
        if(is_array($data)){
            list(
                 $this->presentContinuous->firstPerson,
                 
                 $this->presentContinuous->secondPerson->formal,
                 $this->presentContinuous->secondPerson->semiInformal,
                 $this->presentContinuous->secondPerson->informal,
                 
                 $this->presentContinuous->thirdPerson->formal,
                 $this->presentContinuous->thirdPerson->informal,
                 
                 $this->presentContinuous->impersonal
                 ) = $data;
        }
    }
    
    public function setPastSimple($data){
        if(is_array($data)){
            list(
                 $this->pastSimple->firstPerson,
                 
                 $this->pastSimple->secondPerson->formal,
                 $this->pastSimple->secondPerson->semiInformal,
                 $this->pastSimple->secondPerson->informal,
                 
                 $this->pastSimple->thirdPerson->formal,
                 $this->pastSimple->thirdPerson->informal,
                 
                 $this->pastSimple->impersonal
                 ) = $data;
        }
        
    }
    public function setPastContinuous($data){
        if(is_array($data)){
            list(
                 $this->pastContinuous->firstPerson,
                 
                 $this->pastContinuous->secondPerson->formal,
                 $this->pastContinuous->secondPerson->semiInformal,
                 $this->pastContinuous->secondPerson->informal,
                 
                 $this->pastContinuous->thirdPerson->formal,
                 $this->pastContinuous->thirdPerson->informal,
                 
                 $this->pastContinuous->impersonal
                 ) = $data;
        }
        
    }
    public function setPastHabitual($data){
        if(is_array($data)){
            list(
                 $this->pastHabitual->firstPerson,
                 
                 $this->pastHabitual->secondPerson->formal,
                 $this->pastHabitual->secondPerson->semiInformal,
                 $this->pastHabitual->secondPerson->informal,
                 
                 $this->pastHabitual->thirdPerson->formal,
                 $this->pastHabitual->thirdPerson->informal,
                 
                 $this->pastHabitual->impersonal
                 ) = $data;
        }
    }
    public function setPastConditional($data){
        if(is_array($data)){
            list(
                 $this->pastConditional->firstPerson,
                 
                 $this->pastConditional->secondPerson->formal,
                 $this->pastConditional->secondPerson->semiInformal,
                 $this->pastConditional->secondPerson->informal,
                 
                 $this->pastConditional->thirdPerson->formal,
                 $this->pastConditional->thirdPerson->informal,
                 
                 $this->pastConditional->impersonal
                 ) = $data;
        }
    }

    public function setFutureSimple($data){
        if(is_array($data)){
            list(
                 $this->futureSimple->firstPerson,
                 
                 $this->futureSimple->secondPerson->formal,
                 $this->futureSimple->secondPerson->semiInformal,
                 $this->futureSimple->secondPerson->informal,
                 
                 $this->futureSimple->thirdPerson->formal,
                 $this->futureSimple->thirdPerson->informal,
                 
                 $this->futureSimple->impersonal
                 ) = $data;
        }
    }
    public function setFutureContinuous($data){
        if(is_array($data)){
            list(
                 $this->futureContinuous->firstPerson,
                 
                 $this->futureContinuous->secondPerson->formal,
                 $this->futureContinuous->secondPerson->semiInformal,
                 $this->futureContinuous->secondPerson->informal,
                 
                 $this->futureContinuous->thirdPerson->formal,
                 $this->futureContinuous->thirdPerson->informal,
                 
                 $this->futureContinuous->impersonal
                 ) = $data;
        }
    }

    public function setPerfect($data){
        if(is_array($data)){
            list(
                 $this->perfect->firstPerson,
                 
                 $this->perfect->secondPerson->formal,
                 $this->perfect->secondPerson->semiInformal,
                 $this->perfect->secondPerson->informal,
                 
                 $this->perfect->thirdPerson->formal,
                 $this->perfect->thirdPerson->informal,
                 
                 $this->perfect->impersonal
                 ) = $data;
        }
    }
    public function setPluPerfect($data){
        if(is_array($data)){
            list(
                 $this->pluPerfect->firstPerson,
                 
                 $this->pluPerfect->secondPerson->formal,
                 $this->pluPerfect->secondPerson->semiInformal,
                 $this->pluPerfect->secondPerson->informal,
                 
                 $this->pluPerfect->thirdPerson->formal,
                 $this->pluPerfect->thirdPerson->informal,
                 
                 $this->pluPerfect->impersonal
                 ) = $data;
        }
    }
    
    public function setParticiplePast($data){
        $this->participlePast = $data;
    }
    public function setParticipleConditional($data){
        $this->participleConditional = $data;
    }

    public function setImperativePresent($data){
        if(is_array($data)){
            list(
                 $this->imperativePresent->secondPerson->formal,
                 $this->imperativePresent->secondPerson->semiInformal,
                 $this->imperativePresent->secondPerson->informal,
                 
                 $this->imperativePresent->thirdPerson->formal,
                 $this->imperativePresent->thirdPerson->informal,
                 
                 $this->imperativePresent->impersonal
                 ) = $data;
        }
    }
    public function setImperativeFuture($data){
        if(is_array($data)){
            list(                 
                 $this->imperativeFuture->secondPerson->formal,
                 $this->imperativeFuture->secondPerson->semiInformal,
                 $this->imperativeFuture->secondPerson->informal,
                 
                 $this->imperativeFuture->thirdPerson->formal,
                 $this->imperativeFuture->thirdPerson->informal,
                 
                 $this->imperativeFuture->impersonal
                 ) = $data;
        }
    }

    public function __construct($stem) {
        $this->stem = $stem;
        $this->negative = false;

        $this->presentSimple = new Person();
        $this->presentContinuous = new Person();
        
        $this->pastSimple = new Person();
        $this->pastContinuous = new Person();
        $this->pastConditional = new Person();
        $this->pastHabitual = new Person();

        
        $this->futureSimple = new Person();
        $this->futureContinuous = new Person();

        $this->perfect = new Person();
        $this->pluPerfect = new Person();

        //$this->imperativePresent = new Honorifics2nd();
        //$this->imperativeFuture = new Honorifics2nd();
        $this->imperativePresent = new Person();
        $this->imperativeFuture = new Person();
        
    }
    
    public function conjuate(){
        if($this->negative == true){
            $alphabet = BnChars::$alphabet;
        
            $subject = $this->stem;
            $pattern = "/([{$alphabet}]+)$/u";
            $replace = "না $1";
            $this->stem_negative = preg_replace($pattern, $replace, $subject);    
        }else{
            $this->stem_negative = $this->stem;
        }
        
        $conjugatorFactory = new ConjugatorFactory($this);
        $inflectionRule = $conjugatorFactory->getRule();
        $inflectionRule->conjugateAll();
        
        $this->paradefName = $inflectionRule->paradefName;
    }
}

?>
