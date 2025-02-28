// Create a context menu item
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: 'TextContextMenu',
      title: 'Detect misinformed text',
      contexts: ['selection']
    });

    // Context menu for images
    chrome.contextMenus.create({
        id: 'ImageMenu',
        title: 'Detect deepfake',
        contexts: ['image'],
    });
  });

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'TextContextMenu') {
        // Handle selected text
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: showTextPopup,
            args: [info.selectionText],
        });
    } else if (info.menuItemId === 'ImageMenu') {
        // Handle image URL
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: showImagePopup,
            args: [info.srcUrl],
        });
    }
});

function showTextPopup(selectedText) {
    const overlay = document.createElement('div');
    overlay.className = 'custom-overlay';
  
    // Create popup
    const popup = document.createElement('div');
    popup.className = 'custom-popup';
    popup.textContent = `Selected text: ${selectedText}`;
    overlay.appendChild(popup);

    // Append overlay to body
    document.body.appendChild(overlay);
  
    // Remove overlay on click
    overlay.addEventListener('click', () => {
      document.body.removeChild(overlay);
    });  
}

// Function to display a popup for image URL
function showImagePopup(imageUrl) {
    const overlay = document.createElement('div');
    overlay.className = 'custom-overlay';

    // Create popup
    const img = document.createElement('img');
    img.src = imageUrl;
    img.className = 'custom-popup';
    overlay.appendChild(img);

    // Append overlay to body
    document.body.appendChild(overlay);
  
    // Remove overlay on click
    overlay.addEventListener('click', () => {
      document.body.removeChild(overlay);
    }); 
}

//   // Add a click event listener to the context menu item
//   chrome.contextMenus.onClicked.addListener((info, tab) => {
//     if (info.menuItemId === 'sampleContextMenu') {
//       // Perform an action, e.g., open a new tab with a specific URL
//       chrome.tabs.create({ url: 'https://www.example.com' });
//     }
//   });

//   chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//     if (message.action === 'selectedText') {
//       console.log('Selected text:', message.text);
//       // Perform actions with the selected text, such as storing or displaying it
//     }
//   });