
import ipaddress
import json
import socket
from urllib.parse import urlparse, urljoin

import requests
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

SECURITY_HEADERS = {
    "Content-Security-Policy":
        "Helps reduce certain cross-site scripting risks.",
    "Strict-Transport-Security":
        "Helps browsers enforce HTTPS.",
    "X-Content-Type-Options":
        "Helps prevent MIME-type sniffing.",
    "X-Frame-Options":
        "Helps reduce clickjacking risks.",
    "Referrer-Policy":
        "Controls referrer information sent to other sites.",
    "Permissions-Policy":
        "Controls access to selected browser features."
}


def validate_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError(
            "Enter a valid URL starting with http:// or https://."
        )

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed.")

    host = parsed.hostname

    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            addresses = [
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(
                    host, None, type=socket.SOCK_STREAM
                )
            ]
        except socket.gaierror:
            raise ValueError("Hostname could not be resolved.")

    if not addresses or any(not ip.is_global for ip in addresses):
        raise ValueError("Private or non-public hosts cannot be scanned.")

    return url


def scan_website(url):
    validate_url(url)

    # Fetch one response only; redirects are reported, not followed.
    try:
        response = requests.get(
            url,
            timeout=15,
            allow_redirects=False,
            headers={
                "User-Agent": "Mozilla/5.0 WebShield/1.0",
                "Connection": "close"
            }
        )
    except requests.exceptions.Timeout:
        raise ValueError("The website took too long to respond.")
    except requests.exceptions.ConnectionError:
        raise ValueError(
            "Connection failed. Try another website or check your internet."
        )
    except requests.exceptions.RequestException:
        raise ValueError("Unable to scan this website.")

    try:
        headers = {
            key.lower(): value
            for key, value in response.headers.items()
        }

        findings = []
        score = 100
        submitted_scheme = urlparse(url).scheme.lower()

        # 1. HTTPS check
        if submitted_scheme == "https":
            findings.append({
                "name": "HTTPS",
                "status": "PASS",
                "details": "The submitted URL uses HTTPS."
            })
        else:
            score -= 20
            findings.append({
                "name": "HTTPS",
                "status": "WARNING",
                "details": "The submitted URL uses HTTP, not HTTPS."
            })

        # 2. Redirect check
        redirect_location = headers.get("location")
        redirect_url = (
            urljoin(url, redirect_location)
            if redirect_location else None
        )

        if response.is_redirect or response.is_permanent_redirect:
            findings.append({
                "name": "Redirect",
                "status": "INFO",
                "details": (
                    "Redirect detected. Destination: "
                    + str(redirect_url)
                    + ". It was not requested."
                )
            })

        # 3. Security headers
        for header, explanation in SECURITY_HEADERS.items():
            value = headers.get(header.lower())

            if (
                header == "Strict-Transport-Security"
                and submitted_scheme != "https"
            ):
                findings.append({
                    "name": header,
                    "status": "INFO",
                    "details": (
                        "Test the HTTPS URL to assess the HSTS header."
                    )
                })
            elif value:
                findings.append({
                    "name": header,
                    "status": "PASS",
                    "details": "Header present: " + value[:200]
                })
            else:
                score -= 10
                findings.append({
                    "name": header,
                    "status": "WARNING",
                    "details": "Missing header. " + explanation
                })

        # 4. CORS check
        origin = headers.get("access-control-allow-origin", "")
        credentials = headers.get(
            "access-control-allow-credentials", ""
        ).lower()

        if origin == "*" and credentials == "true":
            score -= 10
            findings.append({
                "name": "CORS",
                "status": "WARNING",
                "details": (
                    "Wildcard origin and credentials=true were returned. "
                    "Review the actual CORS policy."
                )
            })
        elif origin == "*":
            findings.append({
                "name": "CORS",
                "status": "INFO",
                "details": (
                    "Wildcard origin returned. This can be appropriate "
                    "for public resources."
                )
            })
        else:
            findings.append({
                "name": "CORS",
                "status": "INFO",
                "details": (
                    "No wildcard CORS origin detected in this response. "
                    "This does not prove CORS is secure."
                )
            })

        # 5. Cookie attribute check
        cookies = response.raw.headers.getlist("Set-Cookie")

        if not cookies:
            findings.append({
                "name": "Cookie Security",
                "status": "INFO",
                "details": "No Set-Cookie header returned in this response."
            })
        else:
            for cookie in cookies:
                name = cookie.split("=", 1)[0]
                parts = [
                    part.strip().lower()
                    for part in cookie.split(";")
                ]
                missing = []

                if "secure" not in parts:
                    missing.append("Secure")
                if "httponly" not in parts:
                    missing.append("HttpOnly")
                if not any(
                    part.startswith("samesite=") for part in parts
                ):
                    missing.append("SameSite")

                if missing:
                    score -= 5
                    findings.append({
                        "name": "Cookie: " + name[:80],
                        "status": "WARNING",
                        "details": (
                            "Review missing attributes: "
                            + ", ".join(missing)
                        )
                    })
                else:
                    findings.append({
                        "name": "Cookie: " + name[:80],
                        "status": "PASS",
                        "details": (
                            "Secure, HttpOnly and SameSite found."
                        )
                    })

        score = max(0, min(100, score))

        return {
            "url": url,
            "http_status": response.status_code,
            "score": score,
            "findings": findings,
            "redirect_url": redirect_url,
            "note": (
                "Educational configuration score only. It is not a "
                "complete security rating or proof of vulnerability."
            )
        }

    finally:
        response.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url", "").strip()

        try:
            result = scan_website(url)
            return render_template("result.html", result=result)
        except ValueError as error:
            return render_template(
                "index.html", error=str(error)
            ), 400

    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()

    try:
        result = scan_website(url)

        return Response(
            json.dumps(result, indent=2),
            mimetype="application/json",
            headers={
                "Content-Disposition":
                    'attachment; filename="security-report.json"'
            }
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
