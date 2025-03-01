import React, { useState } from "react";

function ImageDetector() {
  const [imageUrl, setImageUrl] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUrlChange = (e) => {
    setImageUrl(e.target.value);
    setSelectedFile(null);
    setPreviewUrl(null);
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setImageUrl("");

      // Create a preview URL for the selected image
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = async () => {
    if (!imageUrl && !selectedFile) return;

    setLoading(true);
    try {
      // In a real implementation, you would send the image to your backend
      // For now, we'll simulate a response
      setTimeout(() => {
        setResult({
          isDeepfake: Math.random() > 0.5,
          confidence: Math.random() * 100,
        });
        setLoading(false);
      }, 1500);

      // Actual implementation would be something like:
      /*
      const formData = new FormData();
      if (selectedFile) {
        formData.append('image', selectedFile);
      } else {
        formData.append('imageUrl', imageUrl);
      }
      
      const response = await fetch('http://127.0.0.1:8000/detect-deepfake/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
      */
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: error.message });
    } finally {
      // setLoading(false); // Uncomment this for the actual implementation
    }
  };

  return (
    <div className="ImageDetector">
      <h3>Deepfake Image Detection</h3>

      <div style={{ marginBottom: "15px" }}>
        <label
          htmlFor="imageUrl"
          style={{ display: "block", marginBottom: "5px" }}
        >
          Image URL:
        </label>
        <input
          type="text"
          id="imageUrl"
          value={imageUrl}
          onChange={handleImageUrlChange}
          placeholder="Enter image URL"
          style={{ width: "100%", padding: "8px", boxSizing: "border-box" }}
          disabled={!!selectedFile}
        />
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label
          htmlFor="imageFile"
          style={{ display: "block", marginBottom: "5px" }}
        >
          Or upload an image:
        </label>
        <input
          type="file"
          id="imageFile"
          accept="image/*"
          onChange={handleFileChange}
          style={{ width: "100%" }}
          disabled={!!imageUrl}
        />
      </div>

      {previewUrl && (
        <div style={{ marginBottom: "15px", textAlign: "center" }}>
          <img
            src={previewUrl}
            alt="Preview"
            style={{ maxWidth: "100%", maxHeight: "200px" }}
          />
        </div>
      )}

      {imageUrl && (
        <div style={{ marginBottom: "15px", textAlign: "center" }}>
          <img
            src={imageUrl}
            alt="From URL"
            style={{ maxWidth: "100%", maxHeight: "200px" }}
            onError={(e) => {
              e.target.onerror = null;
              e.target.style.display = "none";
              alert("Failed to load image from URL");
            }}
          />
        </div>
      )}

      <button
        onClick={analyzeImage}
        disabled={loading || (!imageUrl && !selectedFile)}
        style={{
          padding: "8px 16px",
          backgroundColor: "#9C27B0",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor:
            loading || (!imageUrl && !selectedFile) ? "not-allowed" : "pointer",
          width: "100%",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Image"}
      </button>

      {result && !result.error && (
        <div className="result" style={{ marginTop: "15px" }}>
          <h4>Result:</h4>
          <p>
            This image{" "}
            {result.isDeepfake ? "appears to be" : "does not appear to be"} a
            deepfake.
          </p>
          <p>Confidence: {result.confidence.toFixed(2)}%</p>
        </div>
      )}

      {result && result.error && (
        <div className="error" style={{ marginTop: "15px", color: "red" }}>
          <h4>Error:</h4>
          <p>{result.error}</p>
        </div>
      )}
    </div>
  );
}

export default ImageDetector;
