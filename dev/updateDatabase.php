#!/usr/bin/php
<?php
    require_once "PersistantConnection.class.php";
    
    class DictionaryEntry{
        public $word;
        public $POS;
        public $meanings;
        
        public function __construct($line){
            $splitPattern = "/\t/";
            $wordPOSMeaning = preg_split($splitPattern, $line);
            $wordPOS = preg_split("/:/", $wordPOSMeaning[0]);
            $this->word = preg_replace("/\./", " ", $wordPOS[0]);
            $this->POS = $wordPOS[1];
            
            array_shift($wordPOSMeaning);
            $this->meanings = $wordPOSMeaning;
        }
    }
    
    class Dictionary{
        public $entries;
        
        public function __construct($filename){
            $contents = file_get_contents($filename);
            $pattern = "/\n/";
            $lines = preg_split($pattern, $contents);
            
            $this->entries = array();
            foreach($lines as $line){
                array_push($this->entries, new DictionaryEntry($line));
            }
            
            // safety, remove the last entry, its likely to be empty
            // will include secure check here
            array_pop($this->entries);
        }
    }

    class DatabaseUpdater{
        public $conn;
        public $dic;
        
        public function __construct($conn, $dic){
            try{
                $this->conn = $conn;
                $this->dic = $dic;
                
                $this->conn->exec('SET CHARACTER SET utf8');
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
        
        public function cleanDatabase(){
            try{
                $sql = "DELETE FROM dictionary";
                $stmt = $this->conn->prepare($sql);
                if($stmt->execute()){
                    echo "Cleaned database successfully\n";
                }else{
                    echo "Error in cleaning database\n";
                }        
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }        
        }
        
        
        // just created to check if the code works, that's all
        public function dummy(){
            
            $sql = "INSERT INTO dictionary (id, word, pos, meaning, meaning2, meaning3, meaning4, meaning5)
                    VALUES (:id, :word, :pos, :meaning, :meaning2, :meaning3, :meaning4, :meaning5)";
            $stmt = $this->conn->prepare($sql);
            
            $id = 0;
            $entry = new DictionaryEntry("17-year-old.hippie:NN	১৭ বছর বয়স্ক হিপি");
            $stmt->bindParam(":id", $id);
            $stmt->bindParam(":word", $entry->word);
            $stmt->bindParam(":pos", $entry->POS);
            
            $meaningParam = "বারবার";
            $meaningParam = $entry->meanings[0];
            /*mb_internal_encoding("UTF-8");
            $strlen = mb_strlen($meaningParam);
            $meaningParam = mb_substr($meaningParam, 0, $strlen -1);
            echo $meaningParam;
                      */
            
            $stmt->bindParam(":meaning", $meaningParam);
            $stmt->bindParam(":meaning2", $meaningParam);
            $stmt->bindParam(":meaning3", $meaningParam);
            $stmt->bindParam(":meaning4", $meaningParam);
            $stmt->bindParam(":meaning5", $meaningParam);
            
            if(!$stmt->execute()){
                echo "Error in updating database\n";
            }        
        }
        
        public function updateDatabase(){
            try{
                $this->conn->exec('SET CHARACTER SET utf8');
                
                $sql = "INSERT INTO dictionary (word, pos, meaning, meaning2, meaning3, meaning4, meaning5)
                    VALUES (:word, :pos, :meaning, :meaning2, :meaning3, :meaning4, :meaning5)";
                $stmt = $this->conn->prepare($sql);
                
                foreach($this->dic->entries as $entry){
                    //print_r($entry);

                    $stmt->bindParam(":word", $entry->word);
                    $stmt->bindParam(":pos", $entry->POS);                    
                    
                    if(isset($entry->meanings[0])){
                        $meaning = $entry->meanings[0];
                    }else{
                        $meaning = "";
                    }
                    //echo $meaningParam;
                    $stmt->bindParam(":meaning", $meaning);
                    
                    
                    if(isset($entry->meanings[1])){
                       $meaning2 = $entry->meanings[1];
                    }else{
                        $meaning2 = "";
                    }
                    $stmt->bindParam(":meaning2", $meaning2);
                    
                    
                    
                    if(isset($entry->meanings[2])){
                       $meaning3 = $entry->meanings[2];
                    }else{
                        $meaning3 = "";
                    }
                    $stmt->bindParam(":meaning3", $meaning3);
                    
                    
                    
                    if(isset($entry->meanings[3])){
                       $meaning4 = $entry->meanings[3];
                    }else{
                        $meaning4 = "";
                    }
                    $stmt->bindParam(":meaning4", $meaning4);
                    
                    
                    
                    if(isset($entry->meanings[4])){
                       $meaning5 = $entry->meanings[4];
                    }else{
                        $meaning5 = "";
                    }
                    $stmt->bindParam(":meaning5", $meaning5);
                    
                    if(!$stmt->execute()){
                        echo "Error in updating database for entry {$entry->word}\n ";
                    }        
                }    
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
            
        }
    }
    
    $connection  = PersistantConnection::getConnection();    
    $dictionary = new Dictionary("tagged");
    
    $databaseUpdater = new DatabaseUpdater($connection, $dictionary);
    
    // use with caution
    //$databaseUpdater->cleanDatabase();
    //$databaseUpdater->updateDatabase();
    

    
?>