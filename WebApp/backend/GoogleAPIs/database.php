<?php

function getDB() {
	$dbhost="jamesgtang.com";
	$dbuser="watchmtladmin";
	$dbpass="watchmtl123";
	$dbname="WatchMTL";
	$dbConnection = new PDO("mysql:host=$dbhost;dbname=$dbname;charset=utf8", $dbuser, $dbpass); 
  	$dbConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  	return $dbConnection;
}