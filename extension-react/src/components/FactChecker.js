import React, { useState } from "react";

function FactChecker() {
  const [fact, setFact] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFactChange = (e) => {
    setFact(e.target.value);
  };

  const checkFact = async () => {
    if (!fact.trim()) return;

    setLoading(true);
    try {
      const url = "http://127.0.0.1:8000/fact-check/";
      const response = await fetch(url, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ fact }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="FactChecker">
      <h3>Fact Checker</h3>
      <textarea
        value={fact}
        onChange={handleFactChange}
        placeholder="Enter a fact to check"
        rows={5}
        style={{ width: "100%", marginBottom: "10px" }}
      />
      <button
        onClick={checkFact}
        disabled={loading || !fact.trim()}
        style={{
          padding: "8px 16px",
          backgroundColor: "#2196F3",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: loading || !fact.trim() ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Checking..." : "Check Fact"}
      </button>

      {result && (
        <div className="result" style={{ marginTop: "15px" }}>
          <h4>Result:</h4>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <div>
              <p>{result.result}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default FactChecker;
