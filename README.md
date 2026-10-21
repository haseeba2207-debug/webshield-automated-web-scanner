# 🛡️ WebShield – Automated Web Security Scanner

**A Python Flask-based tool for identifying basic web security misconfigurations.**

WebShield is an educational web security scanning application that analyzes a website's HTTP response and identifies common security weaknesses. It checks HTTPS usage, security headers, cookie protection settings, and Cross-Origin Resource Sharing (CORS) configurations. The application generates a security score and a report of findings to help users understand potential security improvements.

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [How It Works](#how-it-works)
- [Security Checks](#security-checks)
- [Sample Output](#sample-output)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Disclaimer](#disclaimer)
- [Author](#author)

## 📖 Overview

Website security is essential for protecting users, data, and online services. Misconfigured security headers, insecure cookies, and incorrect CORS settings can expose websites to potential risks.

WebShield automates several basic security checks by requesting a website's HTTP response, examining its configuration, and presenting the results in an easy-to-understand format.

This project is intended for learning the fundamentals of web application security, Python programming, and automated security analysis.

## ✨ Features

- **HTTPS Detection:** Checks whether the submitted website uses HTTPS.
- **Security Header Analysis:** Identifies missing recommended HTTP security headers.
- **Cookie Security Analysis:** Checks cookie attributes such as `Secure`, `HttpOnly`, and `SameSite`.
- **CORS Configuration Check:** Identifies potentially unsafe wildcard CORS configurations.
- **HTTP Status Detection:** Displays the HTTP status code returned by the website.
- **Redirect Detection:** Identifies HTTP redirects without automatically following them.
- **Security Score:** Calculates an educational score based on the checks performed.
- **Detailed Findings:** Presents detected issues and recommendations.
- **Report Download:** Allows scan results to be downloaded as a JSON report.
- **URL Validation:** Validates URLs and blocks certain private or non-public destinations to reduce server-side request forgery (SSRF) risks.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming and scanning logic |
| Flask | Web application framework |
| Requests | Sending HTTP requests and receiving responses |
| HTML5 | Creating the user interface |
| CSS3 | Styling the web interface |
| JSON | Exporting scan reports |
| Git and GitHub | Version control and project hosting |

## 📂 Project Structure


automated-web-scanner/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── templates/
    ├── index.html
    └─

**Note:** If you use the standalone submission script, `HaseebaAli_AutomatedWebScanner.py`, it includes the HTML templates within the Python file and does not require the separate `templates` folder.

## ⚙️ Installation

### Prerequisites

- Python 3.10 or later
- pip package manager
- Visual Studio Code or another code editor
- Git (optional, for version control)

### Step 1: Clone the repository

git clone https://github.com/haseeba2207-debug/webshield-automated-web-scanner.git


### Step 2: Open the project folder

cd webshield-automated-web-scanner


### Step 3: Create a virtual environment

**Windows PowerShell:**


python -m venv venv


Activate it:


.\venv\Scripts\Activate.ps1


If PowerShell blocks activation, you can use Command Prompt and ru

venv\Scripts\activate.bat


### Step 4: Install dependencies


python -m pip install -r requirements.txt

## ▶️ How to Run

If you are using the project with `app.py` and the `templates` folder, run:


python app.py


If you are using the standalone submission script instead, run:


python HaseebaAli_AutomatedWebScanner.py


Open your browser and visit:

**http://127.0.0.1:5000**

Enter a website URL you own or are authorized to test, start the scan, and review the results.

## 🔄 How It Works

1. **URL Input:** The user enters a website URL.
2. **URL Validation:** The application validates the URL and checks whether the destination is permitted.
3. **HTTP Request:** Python Requests retrieves the website's HTTP response without automatically following redirects.
4. **Security Analysis:** The scanner examines the response headers, cookies, HTTPS usage, and CORS configuration.
5. **Score Calculation:** A basic score is calculated using the checks performed.
6. **Results Display:** Flask displays the score, HTTP status, and detected findings.
7. **Report Export:** The user can download the scan report in JSON format.

## 🔍 Security Checks

| Check | What it examines |
|---|---|
| HTTPS | Whether the submitted URL uses HTTPS |
| Content-Security-Policy | Helps control permitted content sources |
| Strict-Transport-Security | Helps browsers enforce HTTPS |
| X-Content-Type-Options | Helps prevent MIME-type sniffing |
| X-Frame-Options | Helps mitigate clickjacking |
| Referrer-Policy | Controls referrer information sent by browsers |
| Permissions-Policy | Controls access to selected browser features |
| Cookie attributes | Checks `Secure`, `HttpOnly`, and `SameSite` |
| CORS | Identifies potentially unsafe wildcard-origin and credential combinations |
| HTTP status | Records the response status code |
| Redirects | Reports a redirect destination when available |

## 📊 Sample Output


A scan report may contain:

- Website URL
- HTTP status code
- Security score out of 100
- Missing security headers
- Cookie security findings
- CORS configuration findings
- Redirect information
- Recommendations for improvement

**Important:** The score is an educational indicator based on selected checks. It is not a complete security rating and does not prove that a website is secure or vulnerable.

## ⚠️ Limitations

- The scanner checks a limited set of HTTP-level security configurations.
- Some websites may block automated requests or return connection errors.
- Results depend on the website's current response and configuration.
- A missing header does not always mean a website is vulnerable.
- The scanner does not perform comprehensive penetration testing, authentication testing, or source-code analysis.
- The score is a simplified heuristic and should not be treated as a formal security assessment.

## 🚀 Future Enhancements

- Add more security checks and configurable scanning options.
- Improve the visual presentation of reports.
- Store scan history in a database.
- Generate downloadable PDF reports.
- Add severity levels and remediation guidance.
- Introduce authenticated scanning for authorized test environments.
- Add automated tests and more robust SSRF protection.

## 🔐 Disclaimer

WebShield is developed for educational purposes and authorized security testing only. Scan only websites you own or have explicit permission to test. Do not use this application to conduct unauthorized security assessments.

The tool provides basic configuration checks and is not a substitute for a professional security audit or penetration test.

## 👩‍💻 Author

**Haseeba Feroz Ali**

MSc Blockchain Technology

GitHub: [haseeba2207-debug](https://github.com/haseeba2207-debug)



*WebShield — Identify basic web security misconfigurations and learn how to improve website security.*
