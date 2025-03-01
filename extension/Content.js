// Remove any existing widgets
function removeExistingWidgets() {
  const existingWidgets = document.querySelectorAll(
    ".widget-container, .text-selection-widget, .floating-window"
  );
  existingWidgets.forEach((widget) => widget.remove());
}

// Create and position the widget
function createSelectionWidget(selection) {
  removeExistingWidgets();

  const selectedText = selection.toString().trim();
  if (!selectedText) return;

  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();

  // Create a container for both the widget and menu
  const container = document.createElement("div");
  container.className = "widget-container";
  container.style.position = "absolute";
  container.style.top = `${window.scrollY + rect.bottom + 5}px`;
  container.style.left = `${
    window.scrollX + rect.left + rect.width / 2 - 10
  }px`;
  container.style.zIndex = "9998";

  // Create the widget
  const widget = document.createElement("div");
  widget.className = "text-selection-widget";
  widget.innerHTML = "🔍";
  widget.style.position = "relative";

  // Add hover event to show floating window
  widget.addEventListener("mouseenter", () => {
    createFloatingWindow(container, selectedText);
  });

  container.appendChild(widget);
  document.body.appendChild(container);
}

// Create the floating window with options
function createFloatingWindow(container, selectedText) {
  // Remove any existing floating windows
  const existingWindow = container.querySelector(".floating-window");
  if (existingWindow) existingWindow.remove();

  // Create floating window
  const floatingWindow = document.createElement("div");
  floatingWindow.className = "floating-window";

  // Position it directly above the widget with no gap
  // Since it's in the same container, it will move with the widget when scrolling
  floatingWindow.style.position = "absolute";
  floatingWindow.style.bottom = "24px"; // Position directly above the widget (widget height)
  floatingWindow.style.left = "-88px"; // Center horizontally with the widget

  console.log("Creating floating window in container");

  // Add close button
  const closeButton = document.createElement("div");
  closeButton.className = "close-button";
  closeButton.innerHTML = "✕";
  closeButton.addEventListener("click", (e) => {
    e.stopPropagation();
    floatingWindow.remove();
  });

  // Add options
  const option1 = document.createElement("div");
  option1.className = "option";
  option1.textContent = "Detect AI Text";
  option1.addEventListener("click", () => {
    chrome.runtime.sendMessage({
      action: "checkAIText",
      text: selectedText,
    });
    floatingWindow.remove();
  });

  const option2 = document.createElement("div");
  option2.className = "option";
  option2.textContent = "Fact Check";
  option2.addEventListener("click", () => {
    chrome.runtime.sendMessage({
      action: "factCheck",
      text: selectedText,
    });
    floatingWindow.remove();
  });

  // Assemble the floating window
  floatingWindow.appendChild(closeButton);
  floatingWindow.appendChild(option1);
  floatingWindow.appendChild(option2);

  container.appendChild(floatingWindow);

  // Variable to track if we should hide the menu
  let shouldHideMenu = false;
  let hideMenuTimeout = null;

  // Handle mouse interactions to keep the menu open when moving between widget and menu
  const handleContainerMouseLeave = () => {
    // Set a delay before hiding the menu to give time to move to the menu
    hideMenuTimeout = setTimeout(() => {
      if (shouldHideMenu) {
        floatingWindow.remove();
      }
    }, 300); // 300ms delay
  };

  const handleMenuMouseEnter = () => {
    // Cancel hiding the menu when the mouse enters the menu
    shouldHideMenu = false;
    if (hideMenuTimeout) {
      clearTimeout(hideMenuTimeout);
    }
  };

  const handleMenuMouseLeave = () => {
    // Hide the menu when the mouse leaves the menu
    floatingWindow.remove();
  };

  // Add event listeners
  container.addEventListener("mouseleave", handleContainerMouseLeave);
  floatingWindow.addEventListener("mouseenter", handleMenuMouseEnter);
  floatingWindow.addEventListener("mouseleave", handleMenuMouseLeave);

  // Set initial state
  shouldHideMenu = true;
}

// Listen for text selection
document.addEventListener("mouseup", () => {
  setTimeout(() => {
    const selection = window.getSelection();

    // Check if the user is selecting inside an input or textarea
    const activeElement = document.activeElement;
    if (
      activeElement &&
      (activeElement.tagName === "INPUT" ||
        activeElement.tagName === "TEXTAREA")
    ) {
      const selectedText = activeElement.value
        .substring(activeElement.selectionStart, activeElement.selectionEnd)
        .trim();

      if (selectedText) {
        console.log("Selected text in input:", selectedText);
        // Handle input/textarea selection if needed
      }
    } else if (selection && !selection.isCollapsed) {
      createSelectionWidget(selection);
    }
  }, 10); // Small delay to allow text selection to finalize
});

document.addEventListener("contextmenu", (event) => {
  const clickedElement = event.target;

  // Check if the clicked element is an image
  if (clickedElement.tagName === "IMG") {
    const imageUrl = clickedElement.src;
    console.log("Image URL:", imageUrl);

    // You can also send this to a background script in a Chrome extension:
    // chrome.runtime.sendMessage({ imageUrl });
  }
});

// Create a loading overlay
function createLoadingOverlay(message = "Loading...") {
  // Remove any existing overlays
  const existingOverlays = document.querySelectorAll(".custom-overlay");
  existingOverlays.forEach((overlay) => overlay.remove());

  const overlay = document.createElement("div");
  overlay.className = "custom-overlay";

  const loadingContainer = document.createElement("div");
  loadingContainer.className = "loading-container";

  const spinner = document.createElement("div");
  spinner.className = "loading-spinner";

  const loadingText = document.createElement("div");
  loadingText.className = "loading-text";
  loadingText.textContent = message;

  loadingContainer.appendChild(spinner);
  loadingContainer.appendChild(loadingText);
  overlay.appendChild(loadingContainer);

  document.body.appendChild(overlay);

  return overlay;
}

// Create a custom overlay with close button
function createCustomOverlay(content) {
  // Remove any existing overlays
  const existingOverlays = document.querySelectorAll(".custom-overlay");
  existingOverlays.forEach((overlay) => overlay.remove());

  const overlay = document.createElement("div");
  overlay.className = "custom-overlay";

  const popup = document.createElement("div");
  popup.className = "custom-popup";

  // Add close button
  const closeButton = document.createElement("div");
  closeButton.className = "close-button";
  closeButton.innerHTML = "✕";
  closeButton.addEventListener("click", (e) => {
    e.stopPropagation();
    document.body.removeChild(overlay);
  });

  popup.appendChild(closeButton);

  // Add content
  if (typeof content === "string") {
    const contentDiv = document.createElement("div");
    contentDiv.textContent = content;
    popup.appendChild(contentDiv);
  } else if (content instanceof HTMLElement) {
    popup.appendChild(content);
  }

  overlay.appendChild(popup);
  document.body.appendChild(overlay);

  // Prevent closing when clicking on the popup itself
  popup.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  // Close when clicking on the overlay background
  overlay.addEventListener("click", () => {
    document.body.removeChild(overlay);
  });

  return overlay;
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "showOverlay") {
    createCustomOverlay(request.content);
    sendResponse({ success: true });
  } else if (request.action === "showLoading") {
    createLoadingOverlay(request.message);
    sendResponse({ success: true });
  }
  return true;
});
