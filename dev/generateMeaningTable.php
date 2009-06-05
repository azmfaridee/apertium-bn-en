#!/usr/bin/php
<?php

    require_once "PersistantConnection.class.php";
    require_once "Verb.class.php";

    class MeaningTableUpdater{
        public $conn;
        
        public function __construct($conn){
            $this->conn = $conn;
        }
        
        public function initTable(){            
            try{
                $this->conn->exec('SET CHARACTER SET utf8');
                
                $sql = "SELECT DISTINCT meaning as meaning, word, pos, from dictionary where meaning <> ''
                        union
                        SELECT DISTINCT meaning2 as meaning, word, pos, from dictionary where meaning2 <> ''
                        union
                        SELECT DISTINCT meaning3 as meaning, word, pos, from dictionary where meaning3 <> ''
                        union
                        SELECT DISTINCT meaning4 as meaning, word, pos, from dictionary where meaning4 <> ''
                        union
                        SELECT DISTINCT meaning5 as meaning, word, pos, from dictionary where meaning5 <> ''";
                        
                //echo $sql;
                $stmt = $this->conn->prepare($sql);
                $stmt->execute();
                
                $stmt->bindColumn("meaning", $meaning);
                $stmt->bindColumn("word", $word);                
                $stmt->bindColumn("pos", $pos);
                
                $sqlNoun = "delete from meaning";
                $this->conn->exec($sqlNoun);
                
                $sqlNoun =  "insert into meaning(word, eng_meaning, pos) values(:word, :eng_meaning, :pos)";
                $innerStatement = $this->conn->prepare($sqlNoun);
                
                $innerStatement->bindParam(":word" , $meaning);
                $innerStatement->bindParam(":eng_meaning", $word);
                $innerStatement->bindParam(":pos", $pos);
                
                //$i = 0;
                while($row = $stmt->fetch(PDO::FETCH_BOUND)){
                    if(!$innerStatement->execute()){
                        print_r($stmt->errorInfo());
                    }
                    //echo "$i $meaning $word $extra $pos \n";
                    //$i++;
                }
                
            }catch(PDOException $ex){
                die("ERROR: " . $ex->getMessage());
            }

        }
    }
    
    
    $connection  = PersistantConnection::getConnection();
    
    $meaningTableUpdater = new MeaningTableUpdater($connection);
    $meaningTableUpdater->initTable();
    
?>