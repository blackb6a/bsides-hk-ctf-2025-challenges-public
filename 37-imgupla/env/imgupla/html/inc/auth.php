<?php
include_once(__DIR__ . "/classes/user.class.php");

function getTokenUser() {
    if (empty($_COOKIE['c'])) {
        return null;
    }
    return User::decryptCookie($_COOKIE['c']);
}

function setTokenUser($user) {
    if (empty($user)) {
        return setcookie('c', '');
    }
    return setcookie('c', $user->encryptCookie());
}
