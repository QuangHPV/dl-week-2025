import React, { useState } from "react";
import axios from "axios";
import "../App.css";

function Popup() {
  const [inputText, setInputText] = useState("");
  const [apiType, setApiType] = useState("ai-detection");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let endpoint = "";
      let requestData = {};

      if (apiType === "ai-detection") {
        endpoint = "http://127.0.0.1:8000/check-ai-generated/";
        requestData = { text: inputText };
      } else {
        endpoint = "http://127.0.0.1:8000/fact-check/";
        requestData = { fact: inputText };
      }

      const response = await axios.post(endpoint, requestData, {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.message || "An error occurred");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="Popup">
      <h3>AI Text Analysis Tool</h3>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "10px" }}>
          <label>
            <input
              type="radio"
              name="apiType"
              value="ai-detection"
              checked={apiType === "ai-detection"}
              onChange={() => setApiType("ai-detection")}
            />
            AI Text Detection
          </label>
          <label style={{ marginLeft: "10px" }}>
            <input
              type="radio"
              name="apiType"
              value="fact-check"
              checked={apiType === "fact-check"}
              onChange={() => setApiType("fact-check")}
            />
            Fact Checking
          </label>
        </div>

        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={
            apiType === "ai-detection"
              ? "Enter text to check if AI-generated..."
              : "Enter a fact to check..."
          }
          rows={4}
          style={{ width: "100%", marginBottom: "10px" }}
        />

        <button
          type="submit"
          disabled={loading || !inputText.trim()}
          style={{ padding: "5px 10px" }}
        >
          {loading ? "Processing..." : "Analyze"}
        </button>
      </form>

      {error && (
        <div style={{ color: "red", marginTop: "10px" }}>Error: {error}</div>
      )}

      {result && (
        <div style={{ marginTop: "15px" }}>
          <h4>Result:</h4>
          <pre
            style={{
              whiteSpace: "pre-wrap",
              background: "#f5f5f5",
              padding: "10px",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default Popup;
