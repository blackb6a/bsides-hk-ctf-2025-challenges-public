<?php
include_once(__DIR__ . "/../config.php");

class User {
    private $id;
    private $username;
    private $password;
    
    // Getter methods
    public function getId() {
        return $this->id;
    }

    public function getUsername() {
        return $this->username;
    }

    public function getPassword() {
        return $this->password;
    }

    public function getBio() {
        return $this->bio;
    }

    // Setter methods
    public function setUsername($username) {
        $this->username = $username;
    }

    public function setNewPassword($plaintextPassword) {
        $this->password = password_hash($plaintextPassword, PASSWORD_DEFAULT);
    }

    public function verifyPassword($plaintextPassword) {
        return password_verify($plaintextPassword, $this->password);
    }
    
    public function encryptCookie() {
        global $APP_SECRET;
        $userData = serialize($this);
        $ivSize = openssl_cipher_iv_length('aes-256-ctr');
        $iv = openssl_random_pseudo_bytes($ivSize);
        $cipher = base64_decode(openssl_encrypt($userData, 'aes-256-ctr', $APP_SECRET, 0, $iv));

        return base64_encode($iv . $cipher);
    }

    public static function decryptCookie($encryptedCookie) {
        global $APP_SECRET;
        $data = base64_decode($encryptedCookie);
        $ivSize = openssl_cipher_iv_length('aes-256-ctr');
        $iv = substr($data, 0, $ivSize);
        $cipher = substr($data, $ivSize);

        $decryptedData = openssl_decrypt(base64_encode($cipher), 'aes-256-ctr', $APP_SECRET, 0, $iv);
        return unserialize($decryptedData);
    }
}
