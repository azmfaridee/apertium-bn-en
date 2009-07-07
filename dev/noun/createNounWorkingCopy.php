#!/usr/bin/php

<?php

    /*
    This script uses the rules to generate a working copy of the noun in the data
    -base, we can then use that to directly generate the speling format
    */


    require_once "../config/PersistantConnection.class.php";
    require_once "Noun.class.php";
    require_once "../verb/classes/Misc.class.php";
    
    require_once "nounclasses/NounInflectionRule.class.php";
    
    require_once "nounclasses/NounConjugatorFactory.class.php";
    require_once "nounclasses/NounParadefKeyRule.class.php";
    
    require_once "nounclasses/NounParadefNoRule.class.php";
    require_once "nounclasses/NounParadefBookRule.class.php";
    require_once "nounclasses/NounParadefPenRule.class.php";

        
    class NounUpdater{
        private $conn;
        
        public function __construct($conn){
            try{
                $this->conn = $conn;
                
                $this->conn->exec('SET CHARACTER SET utf8');
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
            
        }
        
        
        public function cleanNounWorkingCopy(){
            try{
                $sql = "delete from noun_working_copy";
                $this->conn->exec($sql);
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
        
        
        public function cleanNounTable(){
            try{
                $sql = "delete from noun_source";
                $this->conn->exec($sql);
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
        
        // this fuction creates the dummy noun table
        public function createDummyNounTable(){
            try{
                //$sql = "SELECT distinct word, eng_meaning, pos FROM meaning m where pos like 'NN' order by word limit 100, 200";
                $sql = "SELECT distinct word FROM meaning m where pos like 'NN' order by word limit 100, 200";
            
                $stmt = $this->conn->prepare($sql);
                $stmt->execute();
                
                $stmt->bindColumn("word", $word);
                //$stmt->bindColumn("eng_meaning", $eng_meaning);
                //$stmt->bindColumn("pos", $pos);
                
                //$sqlInsert = "insert into noun_source(noun, meaning, pos, animacy) values(:noun, :meaning, :pos, :animacy)";
                $sqlInsert = "insert into noun_source(noun, animacy) values(:noun, :animacy)";
                            
                $animacy = "0";
                
                $stmtInsert = $this->conn->prepare($sqlInsert);
                
                $stmtInsert->bindParam(":noun", $word);
                //$stmtInsert->bindParam(":meaning", $eng_meaning);
                //$stmtInsert->bindParam(":pos", $pos);
                $stmtInsert->bindParam(":animacy", $animacy);
                
                while($row = $stmt->fetch(PDO::FETCH_BOUND)){
                    $stmtInsert->execute();
                }
            }
            catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
            
        }
        
        public function inflectNouns(){
            try{
                $sqlSelect = "SELECT lemma, animacy, gender FROM noun_source_freq";
                $stmtSelect = $this->conn->prepare($sqlSelect);
                
                $stmtSelect->bindColumn("lemma", $noun);
                $stmtSelect->bindColumn("animacy", $animacy);
                $stmtSelect->bindColumn("gender", $gender);
                
                $stmtSelect->execute();
                
                /*$sqlInsert = "insert into noun_working_copy(lemma, paradef, animacy, gram_case, number, inflection)
                    VALUES(:lemma, :paradef, :animacy, :gram_case, :number, :inflection)";
                */
                
                
                $sqlInsert = "insert into noun_working_copy(lemma, paradef, animacy, gram_case, number, inflection, gender)
                
                                VALUES(:lemma, :paradef, :animacy, 'nom', 'sg', :nominativeSingular, :gender),
                                    (:lemma, :paradef, :animacy, 'nom', 'sd', :nominativeSingularDet, :gender),
                                    (:lemma, :paradef, :animacy, 'nom', 'pl', :nominativePlural, :gender),
                                    
                                    (:lemma, :paradef, :animacy, 'obj', 'sg', :objectiveSingular, :gender),
                                    (:lemma, :paradef, :animacy, 'obj', 'sd', :objectiveSingularDet, :gender),
                                    (:lemma, :paradef, :animacy, 'obj', 'pl', :objectivePlural, :gender),
                                    
                                    (:lemma, :paradef, :animacy, 'gen', 'sg', :geitiveSingular, :gender),
                                    (:lemma, :paradef, :animacy, 'gen', 'sd', :geitiveSingularDet, :gender),
                                    (:lemma, :paradef, :animacy, 'gen', 'pl', :geitivePlural, :gender),
                                    
                                    (:lemma, :paradef, :animacy, 'loc', 'sg', :locativeSingular, :gender),
                                    (:lemma, :paradef, :animacy, 'loc', 'sd', :locativeSingularDet, :gender),
                                    (:lemma, :paradef, :animacy, 'loc', 'pl', :locativePlural, :gender)
                                    ";
                    
                $stmtInsert = $this->conn->prepare($sqlInsert);
                
                
                while($row = $stmtSelect->fetch(PDO::FETCH_BOUND)){
                    switch($animacy){
                        case("0"):
	                        // inanimate
                            $animacyName = "nn";
                            break;
                        case("1"):
                        	// animate
                            $animacyName = "aa";
                            break;
                        case("2"):
                        	// human
                            $animacyName = "hu";
                            break;
                        case("3"):
                        	// elite
                            $animacyName = "el";
                            break;
                        case("4"):
                        	// animate/inanimate
                            $animacyName = "an";
                    }
                    
                    switch($gender){
                    	case("0"):
                    		// both male and female
                    		$genderName = "mf";
                    		break;
                    	case("1"):
                    		// male
                    		$genderName = "m";
                    		break;
                    	case("2"):
                    		// female
                    		$genderName = "f";
                    		break;                    		
                    	case("3"):
                    		// neutar
                    		$genderName = "nt";
                    		break;
                    	case("3"):
                    		// all
                    		$genderName = "un";
                    		break;                    		                    		
                    }
                    
                    $nounObject = new Noun($noun, $animacy);
                    $nounObject->conjugate();
                    
                    //print_r($nounObject);
                    
                    // bind the varible with current noun
                    $stmtInsert->bindParam(":lemma", $nounObject->stem);
                    $stmtInsert->bindParam(":paradef", $nounObject->ruleName);
                    $stmtInsert->bindParam(":animacy", $animacyName);
                    
                    $stmtInsert->bindParam(":gender", $genderName);
                    
                    $stmtInsert->bindParam(":nominativeSingular", $nounObject->nominative->singular);
                    $stmtInsert->bindParam(":nominativeSingularDet", $nounObject->nominative->singularDet);
                    $stmtInsert->bindParam(":nominativePlural", $nounObject->nominative->plural);
                    
                    $stmtInsert->bindParam(":objectiveSingular", $nounObject->objective->singular);
                    $stmtInsert->bindParam(":objectiveSingularDet", $nounObject->objective->singularDet);
                    $stmtInsert->bindParam(":objectivePlural", $nounObject->objective->plural);
                    
                    $stmtInsert->bindParam(":geitiveSingular", $nounObject->geitive->singular);
                    $stmtInsert->bindParam(":geitiveSingularDet", $nounObject->geitive->singularDet);
                    $stmtInsert->bindParam(":geitivePlural", $nounObject->geitive->plural);
                    
                    
                    $stmtInsert->bindParam(":locativeSingular", $nounObject->locative->singular);
                    $stmtInsert->bindParam(":locativeSingularDet", $nounObject->locative->singularDet);
                    $stmtInsert->bindParam(":locativePlural", $nounObject->locative->plural);
                    
                    $stmtInsert->execute();
                    //print_r($nounObject);
                }
                
                
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
    }

    
    $connection  = PersistantConnection::getConnection();
    $nounUpdater = new NounUpdater($connection);
    
    // use with caution
    //$nounUpdater->cleanNounTable();
    //$nounUpdater->createDummyNounTable();
    $nounUpdater->cleanNounWorkingCopy();
    $nounUpdater->inflectNouns();
      
    
/*    $nounStem = 'চাবি';
    $nounStem = 'পক্ষী';
    $nounStem = 'কৃষ্ণ';
    $noun = new Noun($nounStem, "0");
    $noun->conjugate();
    
    print_r($noun);*/
    
?>
