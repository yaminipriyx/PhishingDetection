import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles.css";

function UrlPhishing() {
  const [url, setUrl] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const validateURL = (input) => {
    try {
      const newUrl = new URL(input);
      return newUrl.protocol === "http:" || newUrl.protocol === "https:";
    } catch {
      return false;
    }
  };

  const handleCheck = async () => {
    setReport(null);
    setError("");

    if (!validateURL(url)) {
      setError("❌ Invalid URL! Enter a valid website.");
      return;
    }
    const fakeReport = {
      safety: Math.random() > 0.5 ? "Safe" : "Phishing",
      confidence: Math.floor(Math.random() * 100) + 1,
      riskFactors: ["SSL Certificate Missing", "Low Trust Score", "Spam Reports Found"],
    };
  
    setReport(fakeReport);

    try {
      const response = await axios.post("http://localhost:5000/analyze", { url });

      if (response.data.status === "error") {
        setError(response.data.message);
      } else {
        setReport({
          safety: response.data.malicious ? "Phishing ⚠️" : "Safe ✅",
          confidence: response.data.malicious ? 90 : 100,
          riskFactors: response.data.malicious
            ? ["🚨 Detected on blacklist", "⚠️ Suspicious domain activity"]
            : ["✅ No suspicious activity found"],
        });
      }
    } catch (error) {
      setError("❌ Error analyzing the website. Try again.");
    }
  };

  return (
    <div className="phishing-container">
      <h1>🔍 Check Website Safety</h1>

      <div className="input-container">
        <input
          type="text"
          placeholder="Enter website URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={handleCheck}>Analyze</button>
      </div>

      {error && <p className="error">{error}</p>}
      {report && (
        <div className="report-card">
          <h2>📊 Website Report</h2>
          <p>Status: <strong>{report.safety}</strong></p>
          <p>Confidence Level: <strong>{report.confidence}%</strong></p>
          <ul>
            {report.riskFactors.map((factor, index) => (
              <li key={index}>⚠️ {factor}</li>
            ))}
          </ul>
          <button onClick={() => navigate("/")}>🔙 Back</button>
        </div>
      )}
    </div>
  );
}

export default UrlPhishing;
