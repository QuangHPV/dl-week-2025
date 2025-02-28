document.addEventListener('mouseup', () => {
  setTimeout(() => { // Delay to ensure selection is finalized
    let selectedText = window.getSelection().toString().trim();

    // Check if the user is selecting inside an input or textarea
    const activeElement = document.activeElement;
    if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
      selectedText = activeElement.value.substring(activeElement.selectionStart, activeElement.selectionEnd).trim();
    }

    if (selectedText) {
      console.log('Selected text:', selectedText);
      // You can also send it to a background script:
      // chrome.runtime.sendMessage({ text: selectedText });
    }
  }, 10); // Small delay to allow text selection to finalize
});