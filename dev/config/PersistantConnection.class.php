<?php

// this class is implemented as a singleton
class PersistantConnection{
    private static $connection = null;
    
    private static $user = "root";
    private static $pass = "root";
    
    private static $database = "bengali_conjugator";
    private static $host = "localhost";
    
    
    public static function getConnection(){
        try{
            if(PersistantConnection::$connection ==  null){
                PersistantConnection::$connection = new PDO(
                                                     "mysql:host=" . PersistantConnection::$host . ";dbname=" . PersistantConnection::$database,
                                                     PersistantConnection::$user,
                                                     PersistantConnection::$pass,
                                                     array( PDO::ATTR_PERSISTENT => true));
            }
            echo "Database Connected\n";
            return PersistantConnection::$connection;
        }catch(PDOException $ex){
            die("ERROR: " . $ex->getMessage());
        }
        
    }
}
?>