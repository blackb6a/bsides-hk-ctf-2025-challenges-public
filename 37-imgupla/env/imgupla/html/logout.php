<?php
    include_once(__DIR__ . "/inc/auth.php");

    setTokenUser(null);
    header("Location: /index.php");
    die();