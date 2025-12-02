# UploadSploit - Burp Suite Extension for File Upload RCE Testing

UploadSploit is a Burp Suite extension designed to automatically test and exploit file upload vulnerabilities, specifically targeting Remote Code Execution (RCE) vulnerabilities through malicious file uploads.

## Features

- Automatic detection of file upload endpoints
- Multiple backend support (PHP, JSP, ASP/ASPX)
- Various bypass techniques (double extensions, null bytes, MIME type manipulation)
- Automatic payload generation and testing
- RCE detection with visual indicators
- Integration with Burp Suite Repeater for manual exploitation

## Installation

1. **Prerequisites**
   - Burp Suite Professional or Community Edition
   - Java Runtime Environment (JRE) installed

2. **Install the Extension**
   - Open Burp Suite
   - Go to **Extensions** tab
   - Click **Add** button
   - Select **Extension type**: Python
   - Click **Select file** and choose `UploadSploit.py`
   - The extension should load successfully (check for "Extension chargée" in the Output tab)

## Usage

### Basic Workflow

1. **Intercept an Upload Request**
   - Navigate to a web application with a file upload feature
   - Upload a legitimate image file (JPG, PNG, or GIF)
   - Ensure Burp Suite Proxy is intercepting requests
   - The upload request should be visible in the Proxy tab

2. **Send to UploadSploit**
   - In Burp Suite Proxy or Repeater, right-click on the intercepted upload request
   - Select **"Envoyer vers UploadSploit"** from the context menu
   - The UploadSploit tab will automatically open and load the request

3. **Configure and Start**
   - The extension will auto-detect the backend (PHP, JSP, or ASP) from the URL
   - Optionally configure:
     - **Backend target**: Select PHP, JSP, ASP, or All
     - **NOT Regex**: Pattern that indicates upload failure (optional)
     - **TRUE Regex**: Pattern that indicates successful code execution (optional)
     - **Uploads path**: Custom upload directory path (optional)
     - **Candidate paths**: Comma-separated list of potential upload directories
   - Click **Start** button to begin automatic scanning

4. **Monitor Results**
   - The central information area displays scan progress and results
   - If RCE is found:
     - The tab title changes to **"UploadSploit [RCE]"**
     - The tab background turns red
     - The progress label shows **"RCE FOUND"** in red
     - The RCE request is automatically sent to Repeater
     - Click **"Replay RCE"** button to resend the successful exploit

### Understanding the Output

- **Information Area**: Shows detected filename, content-type, authentication status, and scan results
- **Request Area**: Displays the selected upload request
- **Progress Label**: Shows scan progress (e.g., "Scan : 50 / 200") and RCE status
- **RCE FOUND Panel**: Appears at the bottom when RCE is detected, with a replay button

## Testing with vuln-app

This repository includes vulnerable applications for testing UploadSploit.

### PHP Application

```bash
cd vuln-app/php
php -S localhost:8080
```

Access the application at `http://localhost:8080`

### JSP Application

```bash
cd vuln-app/jsp
docker build -t uploadsploit-jsp .
docker run -d -p 8080:8080 --name uploadsploit-jsp uploadsploit-jsp
```

Access the application at `http://localhost:8080/vuln-jsp/upload.jsp`

### ASPX Application

```bash
cd vuln-app/aspx
docker build -t uploadsploit-aspx .
docker run -d -p 8081:8081 --name uploadsploit-aspx uploadsploit-aspx
```

Access the application at `http://localhost:8081/Default.aspx`

## Supported Techniques

UploadSploit tests various bypass techniques:

- **Double Extensions**: `file.php.jpg`, `file.jpg.php`
- **Null Byte Injection**: `file.php%00.jpg`, `file.jpg%00.php`
- **MIME Type Manipulation**: Legitimate MIME with malicious extension
- **Case Variations**: `file.PhP`, `file.PHP5`
- **Alternative Extensions**: `phtml`, `php1`, `php2`, `php3`, `php4`, `php5`, `pht`

## Payload Templates

The extension includes several payload templates:

- **phpinfo**: Basic PHP info disclosure
- **nastygif**: GIF header with PHP code
- **nastyjpg**: JPG header with PHP code
- **basicjsp**: JSP code execution test
- **basicaspx**: ASPX code execution test
- **basicasp**: ASP code execution test
- **imagetragick**: ImageTragick vulnerability test
- **htaccess**: .htaccess-based PHP execution

## Troubleshooting

- **Extension not loading**: Ensure Python is properly configured in Burp Suite Extensions settings
- **No context menu**: Make sure you right-click on an intercepted request in Proxy or Repeater
- **Scan not starting**: Verify that a request is loaded in the UploadSploit tab
- **False positives**: Adjust the NOT and TRUE regex patterns to match your target application's responses

## Security Notice

This tool is intended for authorized security testing only. Only use UploadSploit on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal.

## License

This project is provided as-is for educational and authorized security testing purposes.

