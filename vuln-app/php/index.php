<?php
$uploadedPath = "";
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["file"])) {
    $uploadDir = __DIR__ . "/uploads";
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }
    $name = basename($_FILES["file"]["name"]);
    $target = $uploadDir . "/" . $name;
    if (move_uploaded_file($_FILES["file"]["tmp_name"], $target)) {
        $uploadedPath = "/uploads/" . $name;
    }
}
?>
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>PHP Vulnerable Upload</title>
    <script>
        function validateFile() {
            var input = document.getElementById("file");
            if (!input.value) {
                alert("Choose a file");
                return false;
            }
            var allowed = [".png", ".jpg", ".jpeg", ".gif"];
            var name = input.value.toLowerCase();
            var ok = false;
            for (var i = 0; i < allowed.length; i++) {
                if (name.endsWith(allowed[i])) {
                    ok = true;
                }
            }
            if (!ok) {
                alert("Only images allowed");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
<h1>PHP vulnerable upload</h1>
<?php if ($uploadedPath !== ""): ?>
    <p>File uploaded to: <strong><?php echo htmlspecialchars($uploadedPath, ENT_QUOTES, "UTF-8"); ?></strong></p>
    <p>Open this URL in browser to trigger execution if the file is interpreted by PHP.</p>
<?php endif; ?>
<form method="post" enctype="multipart/form-data" onsubmit="return validateFile();">
    <input type="file" id="file" name="file">
    <button type="submit">Upload</button>
</form>
</body>
</html>


