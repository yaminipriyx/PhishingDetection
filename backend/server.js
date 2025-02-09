const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");
const isUrlValid = require("is-url-valid");

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = 5000;

// 🚀 Validate URL before processing
const validateURL = (url) => {
  return isUrlValid(url) && (url.startsWith("http://") || url.startsWith("https://"));
};

// 🚀 API to analyze website safety
app.post("/analyze", async (req, res) => {
  const { url } = req.body;

  if (!validateURL(url)) {
    return res.json({ status: "error", message: "Invalid website URL!" });
  }

  try {
    // 🔍 Call VirusTotal API (replace YOUR_API_KEY)
    const vtResponse = await axios.get(
      `https://www.virustotal.com/api/v3/urls/${encodeURIComponent(url)}`,
      { headers: { "x-apikey": "YOUR_API_KEY" } }
    );

    const { data } = vtResponse;
    const isMalicious = data.data.attributes.last_analysis_stats.malicious > 0;

    res.json({
      status: "success",
      url,
      malicious: isMalicious,
      report: isMalicious ? "⚠️ Phishing detected!" : "✅ Website looks safe!",
    });

  } catch (error) {
    res.json({ status: "error", message: "Could not analyze URL. Try again later." });
  }
});

// Start server
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
