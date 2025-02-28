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


document.addEventListener('contextmenu', (event) => {
  const clickedElement = event.target;

  // Check if the clicked element is an image
  if (clickedElement.tagName === 'IMG') {
    const imageUrl = clickedElement.src;
    console.log('Image URL:', imageUrl);

    // You can also send this to a background script in a Chrome extension:
    // chrome.runtime.sendMessage({ imageUrl });
  }
});