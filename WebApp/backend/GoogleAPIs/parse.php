<?php 
  require 'database.php';
  $db = getDB();
  $user_lat = $request->getParam('latitude');
  $user_long = $request->getParam('longitude');
  $user_time = $request->getParam('timestamp');
  $message = $request->getParam('message');
  try{
    //Verify captcha
    /*
    $post_data = http_build_query(
      array(
        'secret' => "6LcSvDsUAAAAADrn86cZ6nfGAFWn_tgxUogddin9",
        'response' => $_POST['g-recaptcha-response'],
        'remoteip' => $_SERVER['REMOTE_ADDR']
      )
    );
    $opts = array('http' =>
      array(
        'method'  => 'POST',
        'header'  => 'Content-type: application/x-www-form-urlencoded',
        'content' => $post_data
      )
    );
    $context  = stream_context_create($opts);
    $response = file_get_contents('https://www.google.com/recaptcha/api/siteverify', false, $context);
    $result = json_decode($response);
    if (!$result->success) {
        echo "captcha";
    }
    else{*/
    $mtl_lat = 45.5017;
    $mtl_long = -73.5673;
    $earth = 6371; //Earth radius
    $radius = 10; //radius of MTL island
    // Harversine Formula
    $distance_lat = deg2rad($mtl_lat - $user_lat);
    $distance_long = deg2rad($mtl_long - $user_long);
    $a = sin($distance_lat/2) * sin($distance_lat/2) + cos(deg2rad($mtl_lat)) * cos(deg2rad($user_lat)) * sin($distance_long/2) * sin($distance_long/2);
    $c = 2 * asin(sqrt($a));
    $d = $earth * $c;
    // Call Google TimeZone API and retrieve file contents
    $string = 'https://maps.googleapis.com/maps/api/timezone/json?location=' . $user_lat . ',' . $user_long . '&timestamp=1458000000&key=AIzaSyAcT_M6NuZAfszwSSV5mvmw9zD9ut7FwYo';
    //echo $string;
    
    $output = file_get_contents($string);
    $json_a = json_decode($output, true);
    foreach($json_a as $key => $value) {
      if($key == "timeZoneId")
      {
        $city=$value;
      }
    }
    /*$date = new DateTime(null, new DateTimeZone($city));
    echo $timestamp = $date->format('U');*/
    date_default_timezone_set($city);
    $date = date('h:i:s a', time());
    echo $date . ". ";
    //$date = "22:11:11";

    if($d<$radius){
      //echo "within city";
      //Insert issue into DB
      $id = mt_rand();
      $geolocation = $user_lat . "," . $user_long;
      $query = "INSERT INTO `client` (`id`, `issue_id`, `message`, `geolocation`, `time`) VALUES (?, ?, ?, ?, ?)";
      $stmt = $db->prepare($query);
      $stmt->execute([$id, $id, $message, $geolocation, $date]);
      //Call python to check keywords
      #$toescape = './bashPy "There is a flooding." 2>&1';
      #$cmd1 = escapeshellarg($toescape);
      //$cmd1 = './bashPy\ ' . '\"There\ is\ a\ flooding.\"' . '\ 2>\&1';
      //$file='bashPy.txt'
      //$handle = fopen($file, 'a') or die('Cannot open file:  '.$file);
      //$message = " " . $message;
      //fwrite($handle, $message);
      $file = 'bashPy.txt';
      // Open the file to get existing content
      $current = file_get_contents($file);
      // Append a new person to the file
      $current .= $message;
      // Write the contents back to the file
      file_put_contents($file, $current);
      
      echo $cmd1;
      $output= shell_exec($cmd1);

      $f = fopen('output.txt', 'r');
      $line = fgets($f);
      $user_keyword = substr($line, 1, -1);
      fclose($f);
      echo $user_keyword;
      $query = "UPDATE `client` SET `keyword`=? WHERE `id`=?";
      $stmt = $db->prepare($query);
      $stmt->execute([$user_keyword, $id]);

      //$accuracy = substr($python, 0, 2);
      $accuracy = "ok";
      if($accuracy === "ok"){
        //Get issue keyword from DB
        /*$query = "SELECT keyword from client where id=?";
        $stmt = $db->prepare($query);
        $stmt->execute([$id]);
        $key = $stmt->fetch(PDO::FETCH_ASSOC);*/

        $keywords = array();
        $keywords[0] = "fire,tsunami,earthquake,flood,blizzard,snowstorm,hurricane,tornado,wildfire,avalanche,thunderstorm,eruption";
        $keywords[1] = "murder,assassination,homicide,assault,rape,suicide,terrorism,terrorist,stabbing";
        $keywords[2] = "kidnap,kidnapping,hostage,stabbing,";
        $keywords[3] = "theft,mugging,fight,robbery,harassment,threat,arms,armed,gun,accident";
        $keywords[4] = "mischief,disturbance,disturb,assault,";
        $keywords[5] = "traffic,";
        //Check keyword priority
        $i=0;
        $j=99;
        $priority = -1;
        while($i<sizeof($keywords)){
          $keyword_row = explode(',', $keywords[$i]);

          foreach($keyword_row as $value){
            if (strcmp($user_keyword, $value) == 0){
              $query = "UPDATE `client` SET `priority`=? WHERE `id`=?";
              $stmt = $db->prepare($query);
              $stmt->execute([$i, $id]);
            }
          }
          
          $i++;
        }

        //Check if issue has been reported, if yes delete issue
        $query = "SELECT `id`, `geolocation`, `keyword` from client";
        $stmt = $db->prepare($query);
        $stmt->execute();
        $all_loc = $stmt->fetchAll();
        
        foreach($all_loc as $value){
          $other_loc = explode(',', $value['geolocation']);
          $other_lat = $other_loc['0'];
          $other_long = $other_loc['1'];
          $other_id = $value['id'];
          $other_keyword = $value['keyword'];
          $distance_lat = deg2rad($other_lat - $user_lat);
          $distance_long = deg2rad($other_long - $user_long);
          $a = sin($distance_lat/2) * sin($distance_lat/2) + cos(deg2rad($other_lat)) * cos(deg2rad($user_lat)) * sin($distance_long/2) * sin($distance_long/2);
          $c = 2 * asin(sqrt($a));
          $d = $earth * $c;
          
          if($d<0.2){
            if(strcmp($user_keyword, $other_keyword) == 0){
              //echo $id . " " . $other_id . "\n";

              //Delete similar past issues
              $query = "DELETE FROM client where id=? AND id!=?";
              $stmt = $db->prepare($query);
              $stmt->execute([$other_id, $id]);
            }
        
          }
        }
        //Redirect to php file for image checking
        //header("Location: http://localhost/mtlwatch/WebApp/backend/GoogleAPIs/sendinfo.php");
        //exit();
      }
      else{
        $query = "DELETE FROM client where id=?";
        $stmt = $db->prepare($query);
        $stmt->execute([$id]);
        echo "Your report was detected to be inaccurate. Please try again.";
      }
    }
    else{
      echo "You are not reporting from within city bounds. Please try again.";
    }
    
  //}
  }
  catch(Exception $e) {
    echo "Error";
  }
?>