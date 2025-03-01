# React Chrome Extension for AI Content Detection

This project is a React-based Chrome extension that provides tools for detecting AI-generated content, fact-checking information, and analyzing images for potential deepfakes.

## Features

- **Data Viewer**: View extracted post data from web pages
- **AI Text Detector**: Check if text is likely to be AI-generated
- **Fact Checker**: Verify the accuracy of factual claims
- **Image Detector**: Analyze images for potential deepfake manipulation

## Project Structure

The project is organized as follows:

- `public/`: Contains Chrome extension files

  - `manifest.json`: Extension configuration
  - `background.js`: Background script for the extension
  - `content.js`: Content script for the extension
  - `styles.css`: Styles for the extension
  - `index.html`: HTML entry point for the React app

- `src/`: Contains React application files
  - `App.js`: Main application component
  - `index.js`: React entry point
  - `components/`: React components
    - `MainApp.js`: Component that handles tab navigation
    - `Popup.js`: Component for displaying extracted post data
    - `AITextDetector.js`: Component for detecting AI-generated text
    - `FactChecker.js`: Component for fact-checking information
    - `ImageDetector.js`: Component for detecting deepfake images

## Backend API

The extension communicates with a FastAPI backend that provides the following endpoints:

- `/check-ai-generated/`: Detects if text is AI-generated
- `/fact-check/`: Verifies factual claims
- `/get_links/`: Gets relevant links for fact-checking

## Development

### Prerequisites

- Node.js and npm
- Chrome browser

### Installation

1. Clone the repository
2. Install dependencies:

   ```
   cd extension-react
   npm install
   ```

3. Build the extension:

   ```
   npm run build
   ```

4. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `build` directory

### Running the Backend

The backend server needs to be running for the extension to function properly:

1. Navigate to the `fastapi-ai-agent` directory
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the server:
   ```
   uvicorn src.main:app --reload
   ```

## Usage

1. Click on the extension icon to open the popup
2. Use the tabs to navigate between different features:

   - **Data**: View extracted data from the current page
   - **AI Detector**: Paste text to check if it's AI-generated
   - **Fact Checker**: Enter a claim to verify its accuracy
   - **Image Detector**: Upload or provide a URL to an image to check for manipulation

3. Right-click on selected text or images on web pages to access context menu options:
   - "Detect misinformed text"
   - "Fact check information"
   - "Detect deepfake" (for images)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
