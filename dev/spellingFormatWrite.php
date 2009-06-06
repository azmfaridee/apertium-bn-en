#!/usr/bin/php
<?php

require_once "PersistantConnection.class.php";

class SpelingFormatWriter{
    private $fileName;
    private $conn;
    
    public function __construct($fileName, $conn){
        try{
            $this->fileName = $fileName;
            $this->conn = $conn;
            
            $this->conn->exec('SET CHARACTER SET utf8');
        }catch(PDOException $ex){
            die("ERROR: " . $ex->getMessage());
        }
    }
    
    public function getTenseTag($tense){
        switch($tense){
            case("gerund"):
                return "ger";
            case("infinitive"):
                return "inf";
            case("infinitiveAlt"):
                return "inf2";
            case("presentSimple"):
                return "pressmpl";
            case("presentContinuous"):
                return 'prescnt';
            case("pastSimple"):
                return 'pastsmpl';
            case("pastContinuous"):
                return 'pastcont';
            case("pastHabitual"):
                return 'pasthbtl';
            case("pastConditional"):
                return 'pastcnd';
            case("futureSimple"):
                return 'ftsmpl';
            case("futureContinuous"):
                return 'ftcnt';
            case("perfect"):
                return 'prft';
            case("pluPerfect"):
                return 'plprft';
            case("participlePast"):
                return 'ppst';
            case("participleConditional"):
                return 'pcnd';
            case("imperativePresent"):
                return 'presimp';
            case("imperativeFuture"):
                return 'ftimp';
        }
    }
    
    public function getPersonTag($person){
        switch($person){
            case("1st"):
                return "p1";
            case("2nd"):
                return "p2";
            case("3rd"):
                return "p3";
            case("impersonal"):
                return "impr";
            case("none"):
                return '';
        }
    }
    
    public function getPolitenessTag($politeness){
        switch($politeness){
            case("familiar"):
                return "flr";
            case("polite"):
                return "pol";
            case("informal"):
                return "infml";
            case("none"):
                return '';
        }
    }
    
    
    public function writeVerbToFile(){
        $sqlSelect = "SELECT stem, tense, person, politeness, inflection, negative FROM verb";
        
        $stmtSelect = $this->conn->prepare($sqlSelect);
        $stmtSelect->bindColumn("stem", $stem);
        $stmtSelect->bindColumn("tense", $tense);
        $stmtSelect->bindColumn("person", $person);
        $stmtSelect->bindColumn("politeness", $politeness);
        $stmtSelect->bindColumn("inflection", $inflection);
        $stmtSelect->bindColumn("negative", $negative);
        
        $stmtSelect->execute();
        
        $data = "";
        
        while($row = $stmtSelect->fetch(PDO::FETCH_BOUND)){
            //echo "$stem";
            
            $data .= "$stem";
            $data .= "; $inflection";
            
            $str = $this->getTenseTag($tense);
            $data .= "; $str";
            
            $str = $this->getPersonTag($person);
            if($str != ''){
                $data .= ".$str";
            }
            
            $str = $this->getPolitenessTag($politeness);
            if($str != ''){
                $data .= ".$str";
            }
            
            if($negative == 'true'){
                $data .= ".neg";
            }
            
            $data .= "; vblex\n";
            
        }
        
        file_put_contents($this->fileName, $data);
    }
    
    
    public function getCaseTag($case){
        switch($case){
            case("nominative"):
                return "nom";
            case("objective"):
                return "obj";
            case("genitive"):
                return "gen";
            case("locative"):
                return 'loc';
        }
    }
    
    public function getNumberTag($number){
        switch($number){
            case("singular"):
                return "sg";
            case("singularDet"):
                return "sg.det";
            case("plural"):
                return "pl";
        }
    }
    
    public function writeNounToFile(){
        $sqlSelect = "SELECT lemma, gram_case, number, inflection FROM noun_working_copy";
        
        $stmtSelect = $this->conn->prepare($sqlSelect);
        
        $stmtSelect->bindColumn("lemma", $lemma);
        $stmtSelect->bindColumn("gram_case", $gram_case);
        $stmtSelect->bindColumn("number", $number);
        $stmtSelect->bindColumn("inflection", $inflection);
        
        
        $stmtSelect->execute();
        
        $data = "";
        
        while($row = $stmtSelect->fetch(PDO::FETCH_BOUND)){
            // only do, if inflection exists
            
            if($inflection != ''){
                $data .= "$lemma";
                $data .= "; $inflection";
                
                $str = $this->getNumberTag($number);
                if($str != ''){
                    $data .= ".$str";
                }
                
                $str = $this->getCaseTag($gram_case);
                $data .= "; $str";
                
                
                
                $data .= "; n\n";
            }
            
        }
        
        file_put_contents($this->fileName, $data);
    }
    
}

$connection  = PersistantConnection::getConnection();
$spellingFormatWriter = new SpelingFormatWriter('spelingNoun', $connection);
//$spellingFormatWriter->writeVerbToFile();
$spellingFormatWriter->writeNounToFile();
$spellingFormatWriter = new SpelingFormatWriter('spelingVerb', $connection);
$spellingFormatWriter->writeNounToFile();
?>
