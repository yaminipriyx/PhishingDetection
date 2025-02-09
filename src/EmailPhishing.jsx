import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles.css";

function EmailPhishing() {
  const [emailContent, setEmailContent] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleCheck = async () => {
    setReport(null);
    setError("");

    if (!emailContent.trim()) {
      setError("❌ Please enter email content.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/analyze-email", { email: emailContent });

      if (response.data.status === "error") {
        setError(response.data.message);
      } else {
        setReport({
          risk: response.data.risk,
          warnings: response.data.warnings || ["No warnings detected"],
        });
      }
    } catch (error) {
      setError("❌ Error analyzing the email. Try again.");
    }
  };

  return (
    <div className="phishing-container">
      <h1>📧 Check Email Phishing</h1>

      <textarea
        className="styled-input"
        placeholder="Paste email content here..."
        value={emailContent}
        onChange={(e) => setEmailContent(e.target.value)}
      />

      <button className="analyze-btn" onClick={handleCheck}>Analyze</button>

      {error && <p className="error">{error}</p>}
      {report && (
        <div className="report-card">
          <h2>📊 Email Report</h2>
          <p>Risk Level: <strong>{report.risk}</strong></p>
          <ul>
            {report.warnings.map((warning, index) => (
              <li key={index}>⚠️ {warning}</li>
            ))}
          </ul>
        </div>
      )}

      <button className="back-btn" onClick={() => navigate("/")}>🔙 Back</button>
    </div>
  );
}

export default EmailPhishing;
