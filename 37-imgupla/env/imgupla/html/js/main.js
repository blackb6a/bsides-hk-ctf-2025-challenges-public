document.getElementById('choose_image_btn').onclick = function() {
    document.getElementById('file').click();
}
document.getElementById('file').onchange = function() {
    const curFiles = file.files;
    if (curFiles.length === 0) {
        return;
    }
    document.getElementById('choose_image_btn').setAttribute("disabled", "true");
    document.getElementById('choose_image_btn').value = "imgUp!";
    document.getElementById('upload').submit();
}
