<?php

include_once(__DIR__ . "/inc/auth.php");
include_once(__DIR__ . "/inc/db.php");
$error = "";

if (getTokenUser()) {
    header("Location: /index.php");
    die();
}

// Check if the form is submitted
if (isset($_POST['submit'])) {
    // Get user input from the login form
    $username = $_POST['username'];
    $password = $_POST['password'];

    $user = getUserByUsername($username);
    if ($user == null) {
        // if user not exists, register
        $newUser = new User();
        $newUser->setUsername($username);
        $newUser->setNewPassword($password);

        $user = createUser($newUser);
        
    } else {
        // if user exists, login
        if (!$user->verifyPassword($password)) {
            $error = "Incorrect username or password";
            $user = null;
        }
    }

    if ($user) {
        setTokenUser($user);
        header("Location: /index.php");
        die();
    }
}
?>
<?php
include_once(__DIR__ . "/inc/db.php");
include_once(__DIR__ . "/inc/auth.php");
$user = getTokenUser();
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Login - imgUp</title>
  
  <link href="css/bootstrap.min.css" rel="stylesheet">
  <link href="css/styles.css?v=1.6" rel="stylesheet">
  <link href='http://fonts.googleapis.com/css?family=Lato:100,300,400,700,900,100italic,300italic,400italic,700italic,900italic' rel='stylesheet' type='text/css'>
  </head>
  <body>
    <section class="hero" id="hero">
      <?php include(__DIR__ . "/inc/nav.php"); ?>

      <div class="container">
        <div class="row">
          <div class="col-md-2 col-md-offset-5 text-center">
          <br/><br/>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 col-md-offset-3 text-center">
            <h1>Login</h1>
            <form method="post" action="?">
                <label for="username">Username:</label>
                <input type="text" name="username" minlength=3 maxlength=12 required class="form-control"><br>

                <label for="password">Password:</label>
                <input type="password" name="password" minlength=3 required class="form-control"><br>

                <p style="color: red;"><?php echo $error; ?></p>

                <button type="submit" name="submit" class="btn btn-primary">Login/Register</button>
            </form>
          </div>
        </div>
        <div class="row">
          <div class="col-md-2 col-md-offset-5 text-center">
          <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
          </div>
        </div>
      </div>
    </section>
    <footer>
      <div class="container">
        <div class="row">
          <div class="col-md-12 text-center">
            <br/><br/><br/><br/><br/><br/>
            <p class="footer-credit">
              Credit: Design by <a href="http://www.blazrobar.com">Blaz Robar</a><br/>
            </p>
          </div>
        </div>
      </div>
    </footer>
    <script src="/js/main.js"></script>
  </body>
</html>
