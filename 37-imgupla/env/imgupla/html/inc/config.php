<?php

$APP_SECRET = 'secret';
if (isset($_ENV['APP_SECRET'])) {
    $APP_SECRET = $_ENV['APP_SECRET'];
}

$MYSQL_ROOT_PASSWORD = 'password';
if (isset($_ENV['MYSQL_ROOT_PASSWORD'])) {
    $MYSQL_ROOT_PASSWORD = $_ENV['MYSQL_ROOT_PASSWORD'];
}
