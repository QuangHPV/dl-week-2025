# Installing the React Chrome Extension

This guide will walk you through the process of building and installing the React-based Chrome extension.

## Prerequisites

- Node.js and npm installed on your computer
- Google Chrome browser

## Step 1: Build the React Application

1. Open a terminal/command prompt
2. Navigate to the extension-react directory:
   ```
   cd path/to/extension-react
   ```
3. Install the dependencies:
   ```
   npm install
   ```
4. Build the React application:
   ```
   npm run build
   ```
   This will create a `build` directory with the compiled extension files.

## Step 2: Load the Extension in Chrome

1. Open Google Chrome
2. Type `chrome://extensions/` in the address bar and press Enter
3. Enable "Developer mode" by toggling the switch in the top-right corner
4. Click the "Load unpacked" button that appears
5. Navigate to the `build` directory inside your extension-react folder and select it
6. The extension should now be installed and visible in your Chrome toolbar

## Step 3: Start the Backend Server

For the extension to function properly, you need to start the FastAPI backend:

1. Open a new terminal/command prompt
2. Navigate to the fastapi-ai-agent directory:
   ```
   cd path/to/fastapi-ai-agent
   ```
3. Install the Python dependencies (if not already installed):
   ```
   pip install -r requirements.txt
   ```
4. Start the server:
   ```
   uvicorn src.main:app --host 127.0.0.1 --port 8000
   ```
5. The server should now be running at http://127.0.0.1:8000

## Step 4: Using the Extension

1. Click on the extension icon in the Chrome toolbar to open the popup
2. Use the tabs to navigate between different features:

   - **Data**: View extracted data from the current page
   - **AI Detector**: Paste text to check if it's AI-generated
   - **Fact Checker**: Enter a claim to verify its accuracy
   - **Image Detector**: Upload or provide a URL to an image to check for manipulation

3. You can also right-click on selected text or images on web pages to access context menu options:
   - "Detect misinformed text"
   - "Fact check information"
   - "Detect deepfake" (for images)

## Troubleshooting

- If the extension doesn't appear in your toolbar, click the puzzle piece icon and pin it
- If you make changes to the code, you need to rebuild the application and reload the extension
- If the backend API calls fail, make sure the FastAPI server is running
- Check the browser console (F12) for any error messages

## Development Tips

- During development, you can use `npm start` to run the React app in development mode
- After making changes to the extension, you need to:
  1. Rebuild the app with `npm run build`
  2. Go to `chrome://extensions/`
  3. Click the refresh icon on your extension
  4. Reload any open tabs where you're testing the extension
