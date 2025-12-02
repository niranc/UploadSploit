<%@ page import="java.io.*,javax.servlet.*,javax.servlet.http.*" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP Vulnerable Upload</title>
    <meta charset="UTF-8">
    <script type="text/javascript">
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
<h1>JSP vulnerable upload</h1>
<%
    String uploadedPath = null;
    if ("POST".equalsIgnoreCase(request.getMethod())) {
        String contentType = request.getContentType();
        if (contentType != null && contentType.startsWith("multipart/form-data")) {
            ServletInputStream in = request.getInputStream();
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buffer = new byte[4096];
            int read;
            while ((read = in.read(buffer)) != -1) {
                baos.write(buffer, 0, read);
            }
            String body = new String(baos.toByteArray(), "ISO-8859-1");
            String marker = "filename=\"";
            int idx = body.indexOf(marker);
            if (idx != -1) {
                int endIdx = body.indexOf("\"", idx + marker.length());
                if (endIdx != -1) {
                    String fileName = body.substring(idx + marker.length(), endIdx);
                    String boundaryToken = contentType.substring(contentType.indexOf("boundary=") + 9);
                    if (boundaryToken.startsWith("\"") && boundaryToken.endsWith("\"")) {
                        boundaryToken = boundaryToken.substring(1, boundaryToken.length() - 1);
                    }
                    String boundary = "--" + boundaryToken;
                    int dataStart = body.indexOf("\r\n\r\n", endIdx);
                    if (dataStart != -1) {
                        dataStart += 4;
                        int dataEnd = body.indexOf("\r\n" + boundary, dataStart);
                        if (dataEnd != -1) {
                            byte[] all = baos.toByteArray();
                            int offset = dataStart;
                            int length = dataEnd - dataStart;
                            File uploadsDir = new File(application.getRealPath("/uploads"));
                            if (!uploadsDir.exists()) {
                                uploadsDir.mkdirs();
                            }
                            File outFile = new File(uploadsDir, fileName);
                            FileOutputStream fos = new FileOutputStream(outFile);
                            fos.write(all, offset, length);
                            fos.close();
                            uploadedPath = request.getContextPath() + "/uploads/" + fileName;
                        }
                    }
                }
            }
        }
    }
%>
<% if (uploadedPath != null) { %>
    <p>File uploaded to: <strong><%= uploadedPath %></strong></p>
    <p>Browse this URL to trigger execution.</p>
<% } %>
<form method="post" enctype="multipart/form-data" onsubmit="return validateFile();">
    <input type="file" id="file" name="file">
    <button type="submit">Upload</button>
</form>
</body>
</html>


