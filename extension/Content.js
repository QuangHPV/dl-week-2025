  // content.js
  document.addEventListener('mouseup', () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      // Send the selected text to the background script
      chrome.runtime.sendMessage({ action: 'selectedText', text: selectedText });
    }
  });
  