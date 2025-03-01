import React, { useState } from "react";

function AITextDetector() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const checkAIText = async () => {
    if (!text.trim()) return;

    setLoading(true);
    try {
      const url = "http://127.0.0.1:8000/check-ai-generated/";
      const response = await fetch(url, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      console.log(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="AITextDetector">
      <h3>AI Text Detection</h3>
      <textarea
        value={text}
        onChange={handleTextChange}
        placeholder="Enter text to check if it's AI-generated"
        rows={5}
        style={{ width: "100%", marginBottom: "10px" }}
      />
      <button
        onClick={checkAIText}
        disabled={loading || !text.trim()}
        style={{
          padding: "8px 16px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: loading || !text.trim() ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Checking..." : "Check Text"}
      </button>

      {result && (
        <div className="result" style={{ marginTop: "15px" }}>
          <h4>Result:</h4>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <p>
              AI Generated Score: {(result.generated_score * 100).toFixed(2)}%
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default AITextDetector;
