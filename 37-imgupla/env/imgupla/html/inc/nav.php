<?php
include_once(__DIR__ . "/db.php");
include_once(__DIR__ . "/auth.php");
$user = getTokenUser();
?>
        <nav class="navbar">
          <a class="navbar-brand" href="/index.php">imgUpLa</a>
          <ul class="navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="/index.php">Home</a>
            </li>
            <?php if ($user === null): ?>
            <li class="nav-item">
              <a class="nav-link" href="/login.php">Login/Register</a>
            </li>
            <?php else: ?>
            <li class="nav-item">
              <a class="nav-link" href="/logout.php">Logout (<?php echo $user->getUsername(); ?>)</a>
            </li>
            <?php endif; ?>
          </ul>
        </nav>