#!/usr/bin/php
<?php
    require_once "PersistantConnection.class.php";
    
    class Row{
        public $word;
        public $freq;
    }
    
    class FreqLoader{
        private $conn;
        private $entries;
        
        public function __construct($conn, $freqFile){
            $this->conn = $conn;
            $this->conn->exec('SET CHARACTER SET utf8');
            
            $contents = file_get_contents($freqFile);
            
            $pattern = "/\n/";
            $lines = preg_split($pattern, $contents);
            
            $this->entries = array();
            foreach($lines as $line){
                $fields = preg_split("/,/", $line);
                $fields[0] = trim($fields[0], "\"");
                
                array_push($this->entries, $fields);
            }
            array_shift($this->entries);
            array_pop($this->entries);
        }
        
        public function clearFreqTable(){
            try{
                $sql = "delete from frequency";
                $this->conn->exec($sql);
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
        
        public function updateFreqTable(){
            try{
                $sql = "INSERT INTO frequency(word, freq) VALUES(:word, :freq)";
                $stmt = $this->conn->prepare($sql);
                
                
                foreach($this->entries as $entry){
                    $stmt->bindParam(":word", $entry[0]);
                    $stmt->bindParam(":freq", $entry[1]);
                    
                    $stmt->execute();
                }
                
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }
        }
    }

    $connection  = PersistantConnection::getConnection();
    
    $freqFile = "freq.csv";
    $freqLoader = new FreqLoader($connection, $freqFile);
    $freqLoader->clearFreqTable();
    $freqLoader->updateFreqTable();
?>