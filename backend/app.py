from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # <-- Add this line

# Alternatively, you can be specific:
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Common phishing words for emails and SMS
PHISHING_KEYWORDS_EMAIL = [
    "urgent", "verify", "click here", "password", "bank", 
    "suspended", "update account", "login now", "unauthorized"
]
PHISHING_KEYWORDS_SMS = [
    "win", "prize", "claim now", "click link", "otp", "bank", 
    "free", "limited offer", "congratulations", "urgent"
]

# URL phishing detection function
def is_phishing_url(url):
    suspicious_patterns = [
        r"free-\w+", r"login-\w+", r"\.xyz", r"\.top", r"bit\.ly",
        r"tinyurl", r"bank-\w+", r"secure-\w+", r"update-\w+"
    ]
    return any(re.search(pattern, url) for pattern in suspicious_patterns)

@app.route("/")
def home():
    return "Phishing Detection API is running!"

# Email Phishing Detection
@app.route("/analyze-email", methods=["POST"])
def analyze_email():
    data = request.get_json()
    email_content = data.get("email", "")

    if not email_content:
        return jsonify({"status": "error", "message": "No email content provided"}), 400

    warnings = [word for word in PHISHING_KEYWORDS_EMAIL if word in email_content.lower()]
    risk = "High ⚠️" if len(warnings) > 3 else "Medium ⚠️" if len(warnings) > 1 else "Low ✅"

    return jsonify({
        "status": "success",
        "risk": risk,
        "warnings": warnings or ["No major warnings detected."]
    })

# SMS Phishing Detection
@app.route("/analyze-sms", methods=["POST"])
def analyze_sms():
    data = request.get_json()
    sms_content = data.get("sms", "")

    if not sms_content:
        return jsonify({"status": "error", "message": "No SMS content provided"}), 400

    warnings = [word for word in PHISHING_KEYWORDS_SMS if word in sms_content.lower()]
    risk = "High ⚠️" if len(warnings) > 2 else "Medium ⚠️" if len(warnings) > 1 else "Low ✅"

    return jsonify({
        "status": "success",
        "risk": risk,
        "warnings": warnings or ["No major warnings detected."]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
