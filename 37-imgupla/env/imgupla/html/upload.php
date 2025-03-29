<?php

include_once(__DIR__ . "/inc/auth.php");
include_once(__DIR__ . "/inc/db.php");

$user = getTokenUser();
if ($user === null || !isset($_FILES['file'])) {
    header("Location: /index.php");
    die();
}

$uploadDir = 'u/' . $user->getId() . '/';

// Ensure the uploads directory exists
if (!file_exists($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

// Generate a unique filename to avoid overwriting existing files
$uniqueFileName = bin2hex(random_bytes(12)) . '.jpg';
$uploadPath = $uploadDir . $uniqueFileName;

// Move the uploaded file to the server
if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadPath)) {
    // Save upload details to the database
    $upload = new Upload();
    $upload->setFileName($uniqueFileName);
    $upload->setUser($user);
    createUpload($upload);
    
    header("Location: $uploadPath");
} else {
    throw new Exception("Error uploading file.");
}
