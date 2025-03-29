<?php
$flag = 'bsideshk{b4By_x2_13aK??!??!??!}';
$random_number = rand(0, 12);

$result = 'Click to get a random character!';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['index'])) {
    $index = (int) $_POST['index'];

    if ($index >= 0 && $index < strlen($flag)) {
        $char = $flag[$index];
        $result = 'You got character ' . $char . '!';
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Random Character</title>
</head>
<body>
    <h1>Random Character</h1>
    <h3>
    <?php echo $result; ?>
    </h3>
    <form action="" method="POST">
        <input type="hidden" name="index" value="<?php echo $random_number; ?>">
        <button type="submit">Click Me</button>
    </form>
</body>
</html>