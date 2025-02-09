import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles.css";

function SmsPhishing() {
  const [smsContent, setSmsContent] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleCheck = async () => {
    setReport(null);
    setError("");

    if (!smsContent.trim()) {
      setError("❌ Please enter SMS content.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/analyze-sms", { sms: smsContent });

      if (response.data.status === "error") {
        setError(response.data.message);
      } else {
        setReport({
          risk: response.data.risk,
          warnings: response.data.warnings || ["No warnings detected"],
        });
      }
    } catch (error) {
      setError("❌ Error analyzing the SMS. Try again.");
    }
  };

  return (
    <div className="phishing-container">
      <h1>📱 Check SMS Phishing</h1>

      <textarea
        className="styled-input"
        placeholder="Paste SMS content here..."
        value={smsContent}
        onChange={(e) => setSmsContent(e.target.value)}
      />

      <button className="analyze-btn" onClick={handleCheck}>Analyze</button>

      {error && <p className="error">{error}</p>}
      {report && (
        <div className="report-card">
          <h2>📊 SMS Report</h2>
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

export default SmsPhishing;
