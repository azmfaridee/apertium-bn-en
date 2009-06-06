#!/usr/bin/php
<?php

    require_once "PersistantConnection.class.php";
    require_once "Noun.class.php";
    require_once "classes/Misc.class.php";
    
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
                $sqlSelect = "SELECT lemma, animacy FROM noun_source_freq";
                $stmtSelect = $this->conn->prepare($sqlSelect);
                
                $stmtSelect->bindColumn("lemma", $noun);
                $stmtSelect->bindColumn("animacy", $animacy);
                
                $stmtSelect->execute();
                
                /*$sqlInsert = "insert into noun_working_copy(lemma, paradef, animacy, gram_case, number, inflection)
                    VALUES(:lemma, :paradef, :animacy, :gram_case, :number, :inflection)";
                */
                
                
                $sqlInsert = "insert into noun_working_copy(lemma, paradef, animacy, gram_case, number, inflection)
                
                                VALUES(:lemma, :paradef, :animacy, 'nominative', 'singular', :nominativeSingular),
                                    (:lemma, :paradef, :animacy, 'nominative', 'singularDet', :nominativeSingularDet),
                                    (:lemma, :paradef, :animacy, 'nominative', 'plural', :nominativePlural),
                                    
                                    (:lemma, :paradef, :animacy, 'objective', 'singular', :objectiveSingular),
                                    (:lemma, :paradef, :animacy, 'objective', 'singularDet', :objectiveSingularDet),
                                    (:lemma, :paradef, :animacy, 'objective', 'plural', :objectivePlural),
                                    
                                    (:lemma, :paradef, :animacy, 'genitive', 'singular', :geitiveSingular),
                                    (:lemma, :paradef, :animacy, 'genitive', 'singularDet', :geitiveSingularDet),
                                    (:lemma, :paradef, :animacy, 'genitive', 'plural', :geitivePlural),
                                    
                                    (:lemma, :paradef, :animacy, 'locative', 'singular', :locativeSingular),
                                    (:lemma, :paradef, :animacy, 'locative', 'singularDet', :locativeSingularDet),
                                    (:lemma, :paradef, :animacy, 'locative', 'plural', :locativePlural)
                                    ";
                    
                $stmtInsert = $this->conn->prepare($sqlInsert);
                
                
                while($row = $stmtSelect->fetch(PDO::FETCH_BOUND)){
                    switch($animacy){
                        case("0"):
                            $animacyName = "inanimate";
                            break;
                        case("1"):
                            $animacyName = "animate";
                            break;
                        case("2"):
                            $animacyName = "human";
                            break;
                        case("3"):
                            $animacyName = "elite";
                            break;
                    }
                    
                    $nounObject = new Noun($noun, $animacy);
                    $nounObject->conjugate();
                    
                    //print_r($nounObject);
                    
                    // bind the varible with current noun
                    $stmtInsert->bindParam(":lemma", $nounObject->stem);
                    $stmtInsert->bindParam(":paradef", $nounObject->ruleName);
                    $stmtInsert->bindParam(":animacy", $animacyName);
                    
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
