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
    <title>imgUpLa</title>
    
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
            <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
            </div>
          </div>
          <?php if ($user === null): ?>
          <div class="row">
            <div class="col-md-6 col-md-offset-3 text-center">
              <a href="/login.php" class="get-started-btn">Login/Register</a>
            </div>
          </div>
          <?php else: ?>
          <div class="row">
            <div class="col-md-6 col-md-offset-3 text-center">
              <input type="button" id="choose_image_btn" class="get-started-btn" value="Choose an image"/>
              <form id="upload" method="post" action="/upload.php" enctype="multipart/form-data">
                <input type="file" id="file" name="file" class="file" accept="image/jpeg" />
              </form>
              <p>File format: jpg; File size < <?php echo ini_get('upload_max_filesize'); ?></p>
            </div>
          </div>
          <?php endif; ?>
          <div class="row">
            <div class="col-md-2 col-md-offset-5 text-center">
            <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
            </div>
          </div>
        </div>
      </section>
      <footer>
        <div class="container">
          <?php if ($user !== null): ?>
          <div class="row">
            <div class="col-md-4">
              <p><b>Upload history for <?php echo $user->getUsername();?>:</b></p>
            </div>
            <div class="col-md-6">
              <?php
                $uploads = getUploadByUser($user);
                if ($uploads === null) {
                  $uploads = array();
                }
              ?>
              <p><ul>
              <?php foreach ($uploads as &$u): ?>
                <li><a href="u/<?php echo $user->getId() . '/' . $u->getFileName();?>">
                  <?php echo $u->getFileName();?> (<?php echo $u->getDate();?>)
                </a></li>
              <?php endforeach; ?>
              </ul></p>
            </div>
          </div>
          <?php endif; ?>
          <div class="row">
            <div class="col-md-12 text-center">
              <br/><br/><br/><br/><br/><br/>
              <p class="footer-credit">
                Credit: Design by <a href="http://www.blazrobar.com">Blaz Robar</a><br/>
                AI generated images<br/>
              </p>
            </div>
          </div>
        </div>
      </footer>
      <script src="/js/main.js"></script>
    </body>
  </html>
