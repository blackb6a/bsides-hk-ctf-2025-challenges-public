<?php
class Upload {
    private $id;
    private $date;
    private $fileName;
    private $userId;

    // Getter methods
    public function getId() {
        return $this->id;
    }

    public function getDate() {
        return $this->date;
    }

    public function getFileName() {
        return $this->fileName;
    }

    public function getUserId() {
        return $this->userId;
    }

    // Setter methods
    public function setFileName($fileName) {
        $this->fileName = $fileName;
    }

    public function setUser($user) {
        $this->userId = $user->getId();
    }
}
