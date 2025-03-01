import React, { useState } from "react";
import Popup from "./Popup";
import AITextDetector from "./AITextDetector";
import FactChecker from "./FactChecker";
import ImageDetector from "./ImageDetector";

function MainApp() {
  const [activeTab, setActiveTab] = useState("popup");

  const renderTabContent = () => {
    switch (activeTab) {
      case "popup":
        return <Popup />;
      case "aiDetector":
        return <AITextDetector />;
      case "factChecker":
        return <FactChecker />;
      case "imageDetector":
        return <ImageDetector />;
      default:
        return <Popup />;
    }
  };

  return (
    <div className="MainApp">
      <div className="tabs" style={{ display: "flex", marginBottom: "20px" }}>
        <button
          onClick={() => setActiveTab("popup")}
          style={{
            flex: 1,
            padding: "10px",
            backgroundColor: activeTab === "popup" ? "#4CAF50" : "#f1f1f1",
            color: activeTab === "popup" ? "white" : "black",
            border: "none",
            cursor: "pointer",
            borderRadius: "4px 0 0 0",
          }}
        >
          Data
        </button>
        <button
          onClick={() => setActiveTab("aiDetector")}
          style={{
            flex: 1,
            padding: "10px",
            backgroundColor: activeTab === "aiDetector" ? "#4CAF50" : "#f1f1f1",
            color: activeTab === "aiDetector" ? "white" : "black",
            border: "none",
            cursor: "pointer",
            borderRadius: "0 4px 0 0",
          }}
        >
          AI Detector
        </button>
      </div>
      <div className="tabs" style={{ display: "flex", marginBottom: "20px" }}>
        <button
          onClick={() => setActiveTab("factChecker")}
          style={{
            flex: 1,
            padding: "10px",
            backgroundColor:
              activeTab === "factChecker" ? "#4CAF50" : "#f1f1f1",
            color: activeTab === "factChecker" ? "white" : "black",
            border: "none",
            cursor: "pointer",
            borderRadius: "0 0 0 4px",
          }}
        >
          Fact Checker
        </button>
        <button
          onClick={() => setActiveTab("imageDetector")}
          style={{
            flex: 1,
            padding: "10px",
            backgroundColor:
              activeTab === "imageDetector" ? "#4CAF50" : "#f1f1f1",
            color: activeTab === "imageDetector" ? "white" : "black",
            border: "none",
            cursor: "pointer",
            borderRadius: "0 0 4px 0",
          }}
        >
          Image Detector
        </button>
      </div>
      <div className="tab-content">{renderTabContent()}</div>
    </div>
  );
}

export default MainApp;
