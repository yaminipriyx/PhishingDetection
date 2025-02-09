import React, { useState } from "react";
import axios from "axios";
import { Input, Button, Card } from "@/components/ui";

const PhishingDetector = ({ type }) => {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!input) {
      setError("Please enter a valid input");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post(`/api/phishing/${type}`, { input });
      setResult(response.data);
    } catch (err) {
      setError("Failed to fetch results. Please try again.");
    }
    setLoading(false);
  };

  return (
    <Card className="p-6 w-full max-w-md mx-auto shadow-lg rounded-xl">
      <h2 className="text-xl font-semibold mb-4 text-center capitalize">
        {type} Phishing Detection
      </h2>
      <Input
        type="text"
        placeholder={`Enter ${type} here...`}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <Button
        onClick={handleSubmit}
        disabled={loading}
        className="w-full mt-4 bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition"
      >
        {loading ? "Checking..." : "Check for Phishing"}
      </Button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      {result && (
        <p
          className={`mt-4 text-lg font-semibold text-center ${
            result.isPhishing ? "text-red-600" : "text-green-600"
          }`}
        >
          {result.isPhishing ? "⚠️ Phishing Detected!" : "✅ Safe Input"}
        </p>
      )}
    </Card>
  );
};

export default PhishingDetector;
