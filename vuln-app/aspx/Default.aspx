<%@ Page Language="C#" AutoEventWireup="true" Inherits="System.Web.UI.Page" %>
<!DOCTYPE html>
<html>
<head runat="server">
    <title>ASPX Vulnerable Upload</title>
    <script type="text/javascript">
        function validateFile() {
            var input = document.getElementById("FileUpload1");
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
    <form id="form1" runat="server" onsubmit="return validateFile();">
        <div>
            <h1>ASPX vulnerable upload</h1>
            <asp:FileUpload ID="FileUpload1" runat="server" />
            <asp:Button ID="Button1" runat="server" Text="Upload" OnClick="Button1_Click" />
            <br />
            <asp:Label ID="ResultLabel" runat="server" />
        </div>
    </form>
    <script runat="server">
        protected void Button1_Click(object sender, System.EventArgs e)
        {
            if (FileUpload1.HasFile)
            {
                string uploads = Server.MapPath("~/Uploads");
                if (!System.IO.Directory.Exists(uploads))
                {
                    System.IO.Directory.CreateDirectory(uploads);
                }
                string name = System.IO.Path.GetFileName(FileUpload1.FileName);
                string path = System.IO.Path.Combine(uploads, name);
                FileUpload1.SaveAs(path);
                string url = ResolveUrl("~/Uploads/" + name);
                ResultLabel.Text = "File uploaded to: " + url + "<br/>Browse this URL to trigger execution.";
            }
            else
            {
                ResultLabel.Text = "No file selected.";
            }
        }
    </script>
</body>
</html>


