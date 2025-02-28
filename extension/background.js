
// Create a context menu item
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: 'sampleContextMenu',
      title: 'Sample Context Menu',
      contexts: ['all']
    });
  });
  
  // Add a click event listener to the context menu item
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'sampleContextMenu') {
      // Perform an action, e.g., open a new tab with a specific URL
      chrome.tabs.create({ url: 'https://www.example.com' });
    }
  });

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'selectedText') {
      console.log('Selected text:', message.text);
      // Perform actions with the selected text, such as storing or displaying it
    }
  });