<?php

include_once(__DIR__ . "/config.php");
include_once(__DIR__ . "/classes/user.class.php");
include_once(__DIR__ . "/classes/upload.class.php");

$mysqli = new mysqli('127.0.0.1', 'root', $MYSQL_ROOT_PASSWORD, 'imgup');
if($mysqli->connect_error){
    die("Database connection failed: ". $mysqli->connect_error);
}

register_shutdown_function("db_defer");
function db_defer() {
    global $mysqli;
    if (isset($mysqli)) {
        $mysqli->close();
    }
}


// Sanitize user input
foreach ($_POST as $key => $value) {
    $_POST[$key] = $mysqli->real_escape_string($value);
}
foreach ($_GET as $key => $value) {
    $_GET[$key] = $mysqli->real_escape_string($value);
}
foreach ($_REQUEST as $key => $value) {
    $_REQUEST[$key] = $mysqli->real_escape_string($value);
}



function getUserByUsername($username) {
    global $mysqli;

    $sql = "SELECT * FROM users WHERE username = '$username'";
    $result = $mysqli->query($sql);

    if ($result->num_rows > 0) {
        return $result->fetch_object("User");
    }

    return null;
}

function createUser($user) {
    global $mysqli;

    $sql = "INSERT INTO users (username, password)
            VALUES ('{$user->getUsername()}', '{$user->getPassword()}')";
    $result = $mysqli->query($sql);

    if ($result) {
        return getUserByUsername($user->getUsername());
    }

    return null;
}

function getUploadByUser($user) {
    global $mysqli;

    $sql = "SELECT * FROM uploads WHERE userId = {$user->getId()}";
    $result = $mysqli->query($sql);

    if ($result->num_rows > 0) {
        $arr = array();
        while ($obj = $result->fetch_object("Upload")) {
            array_push($arr, $obj);
        }
        return $arr;
    }

    return null;
}

function createUpload($upload) {
    global $mysqli;

    $sql = "INSERT INTO uploads (fileName, userId) 
            VALUES ('{$upload->getFilename()}', {$upload->getUserId()})";
    $result = $mysqli->query($sql);

    if ($result) {
        return true;
    }

    return null;
}
