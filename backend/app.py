from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import joblib  # Import joblib to load ML models
import re
import dns.resolver
import dkim

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the SMS phishing detection model and vectorizer
model = joblib.load("sms_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Common phishing words for emails
PHISHING_KEYWORDS_EMAIL = [
    "urgent", "verify", "click here", "password", "bank", 
    "suspended", "update account", "login now", "unauthorized"
]

VIRUSTOTAL_API_KEY = "db1f9e6093f5dcb4a8ea4de2ea797e74d8e3ff97ed48c148e8c5d307a9b5e1f5"

# URL Phishing Detection (Using VirusTotal)
@app.route("/analyze-url", methods=["POST"])
def analyze_url():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url}", headers=headers)

    if response.status_code == 200:
        result = response.json()
        malicious = result["data"]["attributes"]["last_analysis_stats"]["malicious"]
        safety_status = "Phishing ⚠️" if malicious > 0 else "Safe ✅"

        return jsonify({
            "status": "success",
            "safety": safety_status,
            "confidence": 90 if malicious > 0 else 100,
            "riskFactors": ["🚨 Detected on blacklist"] if malicious > 0 else ["✅ No suspicious activity found"]
        })
    else:
        return jsonify({"status": "error", "message": "VirusTotal API request failed"}), 500

# Email Phishing Detection
def check_spf(domain):
    try:
        answers = dns.resolver.resolve(f"_spf.{domain}", "TXT")
        for txt_record in answers:
            if "v=spf1" in txt_record.to_text():
                return "Valid SPF ✅"
        return "No SPF record found ⚠️"
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return "No SPF record found ⚠️"

def check_dkim(domain, selector="default"):
    try:
        dkim_domain = f"{selector}._domainkey.{domain}"
        answers = dns.resolver.resolve(dkim_domain, "TXT")
        for txt_record in answers:
            if "v=DKIM1" in txt_record.to_text():
                return "Valid DKIM ✅"
        return "No DKIM record found ⚠️"
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return "No DKIM record found ⚠️"

def check_dmarc(domain):
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, "TXT")
        for txt_record in answers:
            if "v=DMARC1" in txt_record.to_text():
                return "Valid DMARC ✅"
        return "No DMARC record found ⚠️"
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return "No DMARC record found ⚠️"

@app.route("/analyze-email", methods=["POST"])
def analyze_email():
    data = request.get_json()
    email_content = data.get("email", "")
    email_header = data.get("header", "")

    if not email_content:
        return jsonify({"status": "error", "message": "No email content provided"}), 400

    match = re.search(r"From:\s*.*?@([\w.-]+)", email_header, re.IGNORECASE)
    domain = match.group(1) if match else None

    if domain:
        spf_result = check_spf(domain)
        dkim_result = check_dkim(domain)
        dmarc_result = check_dmarc(domain)
    else:
        spf_result = dkim_result = dmarc_result = "Could not extract domain ⚠️"

    warnings = [word for word in PHISHING_KEYWORDS_EMAIL if word in email_content.lower()]
    risk = "High ⚠️" if len(warnings) > 3 else "Medium ⚠️" if len(warnings) > 1 else "Low ✅"

    return jsonify({
        "status": "success",
        "risk": risk,
        "warnings": warnings or ["No major warnings detected."],
        "email_authentication": {
            "SPF": spf_result,
            "DKIM": dkim_result,
            "DMARC": dmarc_result
        }
    })

# SMS Phishing Detection (Using ML Model)
@app.route("/analyze-sms", methods=["POST"])
def analyze_sms():
    data = request.get_json()
    sms_content = data.get("sms", "").strip()

    if not sms_content:
        return jsonify({"status": "error", "message": "No SMS content provided"}), 400

    # Vectorize the input SMS
    sms_vectorized = vectorizer.transform([sms_content])

    # Predict using the trained model
    prediction = model.predict(sms_vectorized)[0]  # 0 = Ham, 1 = Spam

    # Convert prediction to readable output
    risk = "Phishing ⚠️" if prediction == 1 else "Safe ✅"

    return jsonify({
        "status": "success",
        "risk": risk,
        "warnings": ["Potential Phishing SMS detected!"] if prediction == 1 else ["No phishing indicators found."]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
