// Create a context menu item
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "TextContextMenu",
    title: "Detect misinformed text",
    contexts: ["selection"],
  });

  chrome.contextMenus.create({
    id: "FactCheckingMenu",
    title: "Fact check information",
    contexts: ["selection"],
  });

  // Context menu for images
  chrome.contextMenus.create({
    id: "ImageMenu",
    title: "Detect deepfake",
    contexts: ["image"],
  });
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "checkAIText") {
    // Show loading overlay first
    chrome.tabs.sendMessage(sender.tab.id, {
      action: "showLoading",
      message: "Analyzing text...",
    });
    checkAIText(request.text, sender.tab.id);
    sendResponse({ success: true });
  } else if (request.action === "factCheck") {
    // Show loading overlay first
    chrome.tabs.sendMessage(sender.tab.id, {
      action: "showLoading",
      message: "Fact checking...",
    });
    factCheck(request.text, sender.tab.id);
    sendResponse({ success: true });
  }
  return true;
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "TextContextMenu") {
    // Show loading overlay first
    chrome.tabs.sendMessage(tab.id, {
      action: "showLoading",
      message: "Analyzing text...",
    });
    // Handle selected text
    checkAIText(info.selectionText, tab.id);
  } else if (info.menuItemId === "ImageMenu") {
    // Show loading overlay first
    chrome.tabs.sendMessage(tab.id, {
        action: "showLoading",
        message: "Scanning image...",
    });
    // Handle image URL
    detectDeepfake(info.srcUrl, tab.id);
  } else if (info.menuItemId === "FactCheckingMenu") {
    // Show loading overlay first
    chrome.tabs.sendMessage(tab.id, {
      action: "showLoading",
      message: "Fact checking...",
    });
    // Handle selected text
    factCheck(info.selectionText, tab.id);
  }
});

async function detectDeepfake(imageUrl, tabId) {
    console.log("Detecting deepfake in image:", imageUrl);
    const url = "http://127.0.0.1:8000/deep_fake/";
    
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image_url: imageUrl }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      

      // Show result using the existing showOverlay function
      if (data.result > 0.99) {
        showOverlay("Your image is highly likely deepfake", tabId);
      } else {
        showOverlay("Your image is likely real", tabId)
      }
    } catch (error) {
      console.error("Error:", error);
      showOverlay(`Error detecting deepfake: ${error.message}`, tabId);
    }
  }
// Function to send a message to the content script to show an overlay
function showOverlay(content, tabId) {
  chrome.tabs.sendMessage(tabId, {
    action: "showOverlay",
    content: content,
  });
}

async function checkAIText(text, tabId) {
  console.log("Checking AI text");
  const url = "http://127.0.0.1:8000/check-ai-generated/";
  try {
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

    
    if (data.generated_score < 0) {
        showOverlay("Text too short, select at least 20 words", tabId);
    } else if (data.generated_score >= 0 && data.generated_score < 0.4) {
        showOverlay("This text is highly likely human-written.", tabId)
    } else if (data.generated_score >= 0.4 && data.generated_score < 0.6) {
        showOverlay("This text is possibly human-written.", tabId)
    } else if (data.generated_score >= 0.6 && data.generated_score < 0.8) {
        showOverlay("This text is possibly AI-generated.", tabId)
    } else {
        showOverlay("This text is highly likely AI-generated.", tabId)
    }
    // Send result to content script to display
    
  } catch (error) {
    console.error("Error:", error);
    showOverlay(`Error checking AI text: ${error.message}`, tabId);
  }
}

async function factCheck(fact, tabId) {
  console.log("Fact checking");
  const url = "http://127.0.0.1:8000/fact-check/";

  try {
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

    // Send result to content script to display
    showOverlay(`Fact check result: ${data.result}`, tabId);
  } catch (error) {
    console.error("Error:", error);
    showOverlay(`Error fact checking: ${error.message}`, tabId);
  }
}
