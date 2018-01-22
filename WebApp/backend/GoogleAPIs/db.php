<?php
use \Psr\Http\Message\ServerRequestInterface as Request;

require '../../../vendor/autoload.php';

$app = new \Slim\App;



$app->post('/parse', function ($request) {
	require 'parse.php';
});

$app->run();
?>