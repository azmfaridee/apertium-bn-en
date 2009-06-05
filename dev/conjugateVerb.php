#!/usr/bin/php
<?php

    require_once "PersistantConnection.class.php";
    require_once "Verb.class.php";

    class VerbUpdater{
        public $conn;
            
        public function __construct($conn){
            $this->conn = $conn;
        }
        
        public function clearVerbs(){
            try{
                $sql = "delete from verb";
                $this->conn->exec($sql);
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
        
        public function updateVerbs(){            
            try{
                $this->conn->exec('SET CHARACTER SET utf8');
                
                $sql = "SELECT distinct word FROM meaning where pos = 'VV'";
                //$sql = "SELECT * from meaning where pos like 'v%' and word = 'পাহারা দে";

                $stmt = $this->conn->prepare($sql);
                $stmt->execute();
                
                $stmt->bindColumn("word", $word);
                
                while($row = $stmt->fetch(PDO::FETCH_BOUND)){
                    $verb = new Verb($word);
                    
                    //echo "$word\n";
                    
                    // conjugete for the positive form
                    $verb->conjuate();
                    
                    $paradefName = $verb->paradefName;
                    
                    $negative = "false";
                    $sqlInsert = "INSERT into verb(stem, paradef, tense, person, politeness, inflection, negative)
                                            VALUES(:stem, :paradef, 'gerund', 'none', 'none', :gerund, :negative),
                                                (:stem, :paradef, 'infinitive', 'none', 'none', :infinitive, :negative),
                                                (:stem, :paradef, 'infinitiveAlt', 'none', 'none', :infinitiveAlt, :negative),
                                                
                                                (:stem, :paradef, 'presentSimple', '1st', 'none', :presentSimple1st, :negative),
                                                (:stem, :paradef, 'presentSimple', '2nd', 'polite', :presentSimple2ndPolite, :negative),
                                                (:stem, :paradef, 'presentSimple', '2nd', 'familiar', :presentSimple2ndFamiliar, :negative),
                                                (:stem, :paradef, 'presentSimple', '2nd', 'informal', :presentSimple2ndInformal, :negative),
                                                (:stem, :paradef, 'presentSimple', '3rd', 'polite', :presentSimple3rdPolite, :negative),
                                                (:stem, :paradef, 'presentSimple', '3rd', 'informal', :presentSimple3rdInformal, :negative),
                                                (:stem, :paradef, 'presentSimple', 'impersonal', 'none', :presentSimpleImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'presentContinuous', '1st', 'none', :presentContinuous1st, :negative),
                                                (:stem, :paradef, 'presentContinuous', '2nd', 'polite', :presentContinuous2ndPolite, :negative),
                                                (:stem, :paradef, 'presentContinuous', '2nd', 'familiar', :presentContinuous2ndFamiliar, :negative),
                                                (:stem, :paradef, 'presentContinuous', '2nd', 'informal', :presentContinuous2ndInformal, :negative),
                                                (:stem, :paradef, 'presentContinuous', '3rd', 'polite', :presentContinuous3rdPolite, :negative),
                                                (:stem, :paradef, 'presentContinuous', '3rd', 'informal', :presentContinuous3rdInformal, :negative),
                                                (:stem, :paradef, 'presentContinuous', 'impersonal', 'none', :presentContinuousImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'pastSimple', '1st', 'none', :pastSimple1st, :negative),
                                                (:stem, :paradef, 'pastSimple', '2nd', 'polite', :pastSimple2ndPolite, :negative),
                                                (:stem, :paradef, 'pastSimple', '2nd', 'familiar', :pastSimple2ndFamiliar, :negative),
                                                (:stem, :paradef, 'pastSimple', '2nd', 'informal', :pastSimple2ndInformal, :negative),
                                                (:stem, :paradef, 'pastSimple', '3rd', 'polite', :pastSimple3rdPolite, :negative),
                                                (:stem, :paradef, 'pastSimple', '3rd', 'informal', :pastSimple3rdInformal, :negative),
                                                (:stem, :paradef, 'pastSimple', 'impersonal', 'none', :pastSimpleImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'pastContinuous', '1st', 'none', :pastContinuous1st, :negative),
                                                (:stem, :paradef, 'pastContinuous', '2nd', 'polite', :pastContinuous2ndPolite, :negative),
                                                (:stem, :paradef, 'pastContinuous', '2nd', 'familiar', :pastContinuous2ndFamiliar, :negative),
                                                (:stem, :paradef, 'pastContinuous', '2nd', 'informal', :pastContinuous2ndInformal, :negative),
                                                (:stem, :paradef, 'pastContinuous', '3rd', 'polite', :pastContinuous3rdPolite, :negative),
                                                (:stem, :paradef, 'pastContinuous', '3rd', 'informal', :pastContinuous3rdInformal, :negative),
                                                (:stem, :paradef, 'pastContinuous', 'impersonal', 'none', :pastContinuousImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'pastHabitual', '1st', 'none', :pastHabitual1st, :negative),
                                                (:stem, :paradef, 'pastHabitual', '2nd', 'polite', :pastHabitual2ndPolite, :negative),
                                                (:stem, :paradef, 'pastHabitual', '2nd', 'familiar', :pastHabitual2ndFamiliar, :negative),
                                                (:stem, :paradef, 'pastHabitual', '2nd', 'informal', :pastHabitual2ndInformal, :negative),
                                                (:stem, :paradef, 'pastHabitual', '3rd', 'polite', :pastHabitual3rdPolite, :negative),
                                                (:stem, :paradef, 'pastHabitual', '3rd', 'informal', :pastHabitual3rdInformal, :negative),
                                                (:stem, :paradef, 'pastHabitual', 'impersonal', 'none', :pastHabitualImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'pastConditional', '1st', 'none', :pastConditional1st, :negative),
                                                (:stem, :paradef, 'pastConditional', '2nd', 'polite', :pastConditional2ndPolite, :negative),
                                                (:stem, :paradef, 'pastConditional', '2nd', 'familiar', :pastConditional2ndFamiliar, :negative),
                                                (:stem, :paradef, 'pastConditional', '2nd', 'informal', :pastConditional2ndInformal, :negative),
                                                (:stem, :paradef, 'pastConditional', '3rd', 'polite', :pastConditional3rdPolite, :negative),
                                                (:stem, :paradef, 'pastConditional', '3rd', 'informal', :pastConditional3rdInformal, :negative),
                                                (:stem, :paradef, 'pastConditional', 'impersonal', 'none', :pastConditionalImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'futureSimple', '1st', 'none', :futureSimple1st, :negative),
                                                (:stem, :paradef, 'futureSimple', '2nd', 'polite', :futureSimple2ndPolite, :negative),
                                                (:stem, :paradef, 'futureSimple', '2nd', 'familiar', :futureSimple2ndFamiliar, :negative),
                                                (:stem, :paradef, 'futureSimple', '2nd', 'informal', :futureSimple2ndInformal, :negative),
                                                (:stem, :paradef, 'futureSimple', '3rd', 'polite', :futureSimple3rdPolite, :negative),
                                                (:stem, :paradef, 'futureSimple', '3rd', 'informal', :futureSimple3rdInformal, :negative),
                                                (:stem, :paradef, 'futureSimple', 'impersonal', 'none', :futureSimpleImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'futureContinuous', '1st', 'none', :futureContinuous1st, :negative),
                                                (:stem, :paradef, 'futureContinuous', '2nd', 'polite', :futureContinuous2ndPolite, :negative),
                                                (:stem, :paradef, 'futureContinuous', '2nd', 'familiar', :futureContinuous2ndFamiliar, :negative),
                                                (:stem, :paradef, 'futureContinuous', '2nd', 'informal', :futureContinuous2ndInformal, :negative),
                                                (:stem, :paradef, 'futureContinuous', '3rd', 'polite', :futureContinuous3rdPolite, :negative),
                                                (:stem, :paradef, 'futureContinuous', '3rd', 'informal', :futureContinuous3rdInformal, :negative),
                                                (:stem, :paradef, 'futureContinuous', 'impersonal', 'none', :futureContinuousImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'perfect', '1st', 'none', :perfect1st, :negative),
                                                (:stem, :paradef, 'perfect', '2nd', 'polite', :perfect2ndPolite, :negative),
                                                (:stem, :paradef, 'perfect', '2nd', 'familiar', :perfect2ndFamiliar, :negative),
                                                (:stem, :paradef, 'perfect', '2nd', 'informal', :perfect2ndInformal, :negative),
                                                (:stem, :paradef, 'perfect', '3rd', 'polite', :perfect3rdPolite, :negative),
                                                (:stem, :paradef, 'perfect', '3rd', 'informal', :perfect3rdInformal, :negative),
                                                (:stem, :paradef, 'perfect', 'impersonal', 'none', :perfectImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'pluPerfect', '1st', 'none', :pluPerfect1st, :negative),
                                                (:stem, :paradef, 'pluPerfect', '2nd', 'polite', :pluPerfect2ndPolite, :negative),
                                                (:stem, :paradef, 'pluPerfect', '2nd', 'familiar', :pluPerfect2ndFamiliar, :negative),
                                                (:stem, :paradef, 'pluPerfect', '2nd', 'informal', :pluPerfect2ndInformal, :negative),
                                                (:stem, :paradef, 'pluPerfect', '3rd', 'polite', :pluPerfect3rdPolite, :negative),
                                                (:stem, :paradef, 'pluPerfect', '3rd', 'informal', :pluPerfect3rdInformal, :negative),
                                                (:stem, :paradef, 'pluPerfect', 'impersonal', 'none', :pluPerfectImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'participlePast', 'none', 'none', :participlePast, :negative),
                                                (:stem, :paradef, 'participleConditional', 'none', 'none', :participleConditional, :negative),
                                                
                                                (:stem, :paradef, 'imperativePresent', '2nd', 'polite', :imperativePresent2ndPolite, :negative),
                                                (:stem, :paradef, 'imperativePresent', '2nd', 'familiar', :imperativePresent2ndFamiliar, :negative),
                                                (:stem, :paradef, 'imperativePresent', '2nd', 'informal', :imperativePresent2ndInformal, :negative),
                                                (:stem, :paradef, 'imperativePresent', '3rd', 'polite', :imperativePresent3rdPolite, :negative),
                                                (:stem, :paradef, 'imperativePresent', '3rd', 'informal', :imperativePresent3rdInformal, :negative),
                                                (:stem, :paradef, 'imperativePresent', 'impersonal', 'none', :imperativePresentImpersonal, :negative),
                                                
                                                (:stem, :paradef, 'imperativeFuture', '2nd', 'polite', :imperativeFuture2ndPolite, :negative),
                                                (:stem, :paradef, 'imperativeFuture', '2nd', 'familiar', :imperativeFuture2ndFamiliar, :negative),
                                                (:stem, :paradef, 'imperativeFuture', '2nd', 'informal', :imperativeFuture2ndInformal, :negative),
                                                (:stem, :paradef, 'imperativeFuture', '3rd', 'polite', :imperativeFuture3rdPolite, :negative),
                                                (:stem, :paradef, 'imperativeFuture', '3rd', 'informal', :imperativeFuture3rdInformal, :negative),
                                                (:stem, :paradef, 'imperativeFuture', 'impersonal', 'none', :imperativeFutureImpersonal, :negative)";
                                                
                    $stmtInsert = $this->conn->prepare($sqlInsert);
                    $stmtInsert->bindParam(":stem", $word);                    
                    $stmtInsert->bindParam(":paradef", $verb->paradefName);
                    $stmtInsert->bindParam(":negative", $negative);
                    
                    $stmtInsert->bindParam(":infinitive", $verb->infinitive);
                    $stmtInsert->bindParam(":gerund", $verb->gerund);
                    $stmtInsert->bindParam(":infinitiveAlt", $verb->infinitiveAlt);
                    
                    $stmtInsert->bindParam(":presentSimple1st", $verb->presentSimple->firstPerson);
                    $stmtInsert->bindParam(":presentSimple2ndPolite", $verb->presentSimple->secondPerson->formal);
                    $stmtInsert->bindParam(":presentSimple2ndFamiliar", $verb->presentSimple->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":presentSimple2ndInformal", $verb->presentSimple->secondPerson->informal);
                    $stmtInsert->bindParam(":presentSimple3rdPolite", $verb->presentSimple->thirdPerson->formal);
                    $stmtInsert->bindParam(":presentSimple3rdInformal", $verb->presentSimple->thirdPerson->informal);
                    $stmtInsert->bindParam(":presentSimpleImpersonal", $verb->presentSimple->impersonal);
                    
                    $stmtInsert->bindParam(":presentContinuous1st", $verb->presentContinuous->firstPerson);
                    $stmtInsert->bindParam(":presentContinuous2ndPolite", $verb->presentContinuous->secondPerson->formal);
                    $stmtInsert->bindParam(":presentContinuous2ndFamiliar", $verb->presentContinuous->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":presentContinuous2ndInformal", $verb->presentContinuous->secondPerson->informal);
                    $stmtInsert->bindParam(":presentContinuous3rdPolite", $verb->presentContinuous->thirdPerson->formal);
                    $stmtInsert->bindParam(":presentContinuous3rdInformal", $verb->presentContinuous->thirdPerson->informal);
                    $stmtInsert->bindParam(":presentContinuousImpersonal", $verb->presentContinuous->impersonal);
                    
                    $stmtInsert->bindParam(":pastSimple1st", $verb->pastSimple->firstPerson);
                    $stmtInsert->bindParam(":pastSimple2ndPolite", $verb->pastSimple->secondPerson->formal);
                    $stmtInsert->bindParam(":pastSimple2ndFamiliar", $verb->pastSimple->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":pastSimple2ndInformal", $verb->pastSimple->secondPerson->informal);
                    $stmtInsert->bindParam(":pastSimple3rdPolite", $verb->pastSimple->thirdPerson->formal);
                    $stmtInsert->bindParam(":pastSimple3rdInformal", $verb->pastSimple->thirdPerson->informal);
                    $stmtInsert->bindParam(":pastSimpleImpersonal", $verb->pastSimple->impersonal);
                    
                    $stmtInsert->bindParam(":pastContinuous1st", $verb->pastContinuous->firstPerson);
                    $stmtInsert->bindParam(":pastContinuous2ndPolite", $verb->pastContinuous->secondPerson->formal);
                    $stmtInsert->bindParam(":pastContinuous2ndFamiliar", $verb->pastContinuous->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":pastContinuous2ndInformal", $verb->pastContinuous->secondPerson->informal);
                    $stmtInsert->bindParam(":pastContinuous3rdPolite", $verb->pastContinuous->thirdPerson->formal);
                    $stmtInsert->bindParam(":pastContinuous3rdInformal", $verb->pastContinuous->thirdPerson->informal);
                    $stmtInsert->bindParam(":pastContinuousImpersonal", $verb->pastContinuous->impersonal);
                    
                    $stmtInsert->bindParam(":pastHabitual1st", $verb->pastHabitual->firstPerson);
                    $stmtInsert->bindParam(":pastHabitual2ndPolite", $verb->pastHabitual->secondPerson->formal);
                    $stmtInsert->bindParam(":pastHabitual2ndFamiliar", $verb->pastHabitual->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":pastHabitual2ndInformal", $verb->pastHabitual->secondPerson->informal);
                    $stmtInsert->bindParam(":pastHabitual3rdPolite", $verb->pastHabitual->thirdPerson->formal);
                    $stmtInsert->bindParam(":pastHabitual3rdInformal", $verb->pastHabitual->thirdPerson->informal);
                    $stmtInsert->bindParam(":pastHabitualImpersonal", $verb->pastHabitual->impersonal);
                    
                    $stmtInsert->bindParam(":pastConditional1st", $verb->pastConditional->firstPerson);
                    $stmtInsert->bindParam(":pastConditional2ndPolite", $verb->pastConditional->secondPerson->formal);
                    $stmtInsert->bindParam(":pastConditional2ndFamiliar", $verb->pastConditional->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":pastConditional2ndInformal", $verb->pastConditional->secondPerson->informal);
                    $stmtInsert->bindParam(":pastConditional3rdPolite", $verb->pastConditional->thirdPerson->formal);
                    $stmtInsert->bindParam(":pastConditional3rdInformal", $verb->pastConditional->thirdPerson->informal);
                    $stmtInsert->bindParam(":pastConditionalImpersonal", $verb->pastConditional->impersonal);
                    
                    $stmtInsert->bindParam(":futureSimple1st", $verb->futureSimple->firstPerson);
                    $stmtInsert->bindParam(":futureSimple2ndPolite", $verb->futureSimple->secondPerson->formal);
                    $stmtInsert->bindParam(":futureSimple2ndFamiliar", $verb->futureSimple->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":futureSimple2ndInformal", $verb->futureSimple->secondPerson->informal);
                    $stmtInsert->bindParam(":futureSimple3rdPolite", $verb->futureSimple->thirdPerson->formal);
                    $stmtInsert->bindParam(":futureSimple3rdInformal", $verb->futureSimple->thirdPerson->informal);
                    $stmtInsert->bindParam(":futureSimpleImpersonal", $verb->futureSimple->impersonal);
                    
                    $stmtInsert->bindParam(":futureContinuous1st", $verb->futureContinuous->firstPerson);
                    $stmtInsert->bindParam(":futureContinuous2ndPolite", $verb->futureContinuous->secondPerson->formal);
                    $stmtInsert->bindParam(":futureContinuous2ndFamiliar", $verb->futureContinuous->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":futureContinuous2ndInformal", $verb->futureContinuous->secondPerson->informal);
                    $stmtInsert->bindParam(":futureContinuous3rdPolite", $verb->futureContinuous->thirdPerson->formal);
                    $stmtInsert->bindParam(":futureContinuous3rdInformal", $verb->futureContinuous->thirdPerson->informal);
                    $stmtInsert->bindParam(":futureContinuousImpersonal", $verb->futureContinuous->impersonal);
                    
                    $stmtInsert->bindParam(":perfect1st", $verb->perfect->firstPerson);
                    $stmtInsert->bindParam(":perfect2ndPolite", $verb->perfect->secondPerson->formal);
                    $stmtInsert->bindParam(":perfect2ndFamiliar", $verb->perfect->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":perfect2ndInformal", $verb->perfect->secondPerson->informal);
                    $stmtInsert->bindParam(":perfect3rdPolite", $verb->perfect->thirdPerson->formal);
                    $stmtInsert->bindParam(":perfect3rdInformal", $verb->perfect->thirdPerson->informal);
                    $stmtInsert->bindParam(":perfectImpersonal", $verb->perfect->impersonal);
                    
                    $stmtInsert->bindParam(":pluPerfect1st", $verb->pluPerfect->firstPerson);
                    $stmtInsert->bindParam(":pluPerfect2ndPolite", $verb->pluPerfect->secondPerson->formal);
                    $stmtInsert->bindParam(":pluPerfect2ndFamiliar", $verb->pluPerfect->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":pluPerfect2ndInformal", $verb->pluPerfect->secondPerson->informal);
                    $stmtInsert->bindParam(":pluPerfect3rdPolite", $verb->pluPerfect->thirdPerson->formal);
                    $stmtInsert->bindParam(":pluPerfect3rdInformal", $verb->pluPerfect->thirdPerson->informal);
                    $stmtInsert->bindParam(":pluPerfectImpersonal", $verb->pluPerfect->impersonal);
                    
                    $stmtInsert->bindParam(":participlePast", $verb->participlePast);
                    $stmtInsert->bindParam(":participleConditional", $verb->participleConditional);
                    
                    $stmtInsert->bindParam(":imperativePresent2ndPolite", $verb->imperativePresent->secondPerson->formal);
                    $stmtInsert->bindParam(":imperativePresent2ndFamiliar", $verb->imperativePresent->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":imperativePresent2ndInformal", $verb->imperativePresent->secondPerson->informal);
                    $stmtInsert->bindParam(":imperativePresent3rdPolite", $verb->imperativePresent->thirdPerson->formal);
                    $stmtInsert->bindParam(":imperativePresent3rdInformal", $verb->imperativePresent->thirdPerson->informal);
                    $stmtInsert->bindParam(":imperativePresentImpersonal", $verb->imperativePresent->impersonal);
                    
                    $stmtInsert->bindParam(":imperativeFuture2ndPolite", $verb->imperativeFuture->secondPerson->formal);
                    $stmtInsert->bindParam(":imperativeFuture2ndFamiliar", $verb->imperativeFuture->secondPerson->semiInformal);
                    $stmtInsert->bindParam(":imperativeFuture2ndInformal", $verb->imperativeFuture->secondPerson->informal);
                    $stmtInsert->bindParam(":imperativeFuture3rdPolite", $verb->imperativeFuture->thirdPerson->formal);
                    $stmtInsert->bindParam(":imperativeFuture3rdInformal", $verb->imperativeFuture->thirdPerson->informal);
                    $stmtInsert->bindParam(":imperativeFutureImpersonal", $verb->imperativeFuture->impersonal);
                    
                    $stmtInsert->execute();
                 
                    // conjugate for the negative form
                    $verb->negative = true;
                    $negative = "true";
                    $verb->conjuate();
                    
                    $stmtInsert->execute();
                }
                
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }

        }
    }
    
    
    $connection  = PersistantConnection::getConnection();
    
    $verbUpdater = new VerbUpdater($connection);
    $verbUpdater->clearVerbs();
    $verbUpdater->updateVerbs();
    
?>