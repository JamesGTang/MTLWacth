<?php 
  require 'database.php';
  $db = getDB();
  

  try{
    $query = "SELECT FROM `client` VALUES (?)";
    $stmt = $db->prepare($query);
    $stmt->execute([$message]);
    echo '<script language="javascript">';
    echo 'alert("message successfully sent")';
    echo '</script>';

    

  }
  catch(Exception $e) {
    echo "Error";
  }
?>