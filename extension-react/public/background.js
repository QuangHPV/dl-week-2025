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

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "TextContextMenu") {
    // Handle selected text
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: checkAIText,
      args: [info.selectionText],
    });
  } else if (info.menuItemId === "ImageMenu") {
    // Handle image URL
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: showImagePopup,
      args: [info.srcUrl],
    });
  } else if (info.menuItemId === "FactCheckingMenu") {
    // Handle image URL
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: factCheck,
      args: [info.selectionText],
    });
  }
});

// Function to display a popup for image URL
function showImagePopup(imageUrl) {
  const overlay = document.createElement("div");
  overlay.className = "custom-overlay";

  // Create popup
  const img = document.createElement("img");
  img.src = imageUrl;
  img.className = "custom-popup";
  overlay.appendChild(img);

  // Append overlay to body
  document.body.appendChild(overlay);

  // Remove overlay on click
  overlay.addEventListener("click", () => {
    document.body.removeChild(overlay);
  });
}

async function checkAIText(text) {
  console.log("After request");
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
    //return data.result;  // Extracting the "result" attribute
    const overlay = document.createElement("div");
    overlay.className = "custom-overlay";

    // Create popup
    const popup = document.createElement("div");
    popup.className = "custom-popup";
    popup.textContent = `Selected text: ${text}\nResult:${data.result}`;
    overlay.appendChild(popup);

    // Append overlay to body
    document.body.appendChild(overlay);

    // Remove overlay on click
    overlay.addEventListener("click", () => {
      document.body.removeChild(overlay);
    });
  } catch (error) {
    console.error("Error:", error);
  }
}

async function factCheck(fact) {
  const url = "http://127.0.0.1:8000/fact-check/";
  console.log("After request");
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
    //return data.result;  // Extracting the "result" attribute
    const overlay = document.createElement("div");
    overlay.className = "custom-overlay";

    // Create popup
    const popup = document.createElement("div");
    popup.className = "custom-popup";
    popup.textContent = `Result:${data.result}`;
    overlay.appendChild(popup);

    // Append overlay to body
    document.body.appendChild(overlay);

    // Remove overlay on click
    overlay.addEventListener("click", () => {
      document.body.removeChild(overlay);
    });
  } catch (error) {
    console.error("Error:", error);
  }
}
