# FastAPI AI Agent

This project is a FastAPI application designed to serve as an AI agent for checking misinformation and detecting AI-generated content. It provides endpoints to analyze highlighted text from websites and returns the results of the analysis.

## Project Structure

```
fastapi-ai-agent
├── src
│   ├── main.py          # Entry point of the FastAPI application
│   ├── agent.py         # Logic for detecting misinformation and AI-generated content
│   └── models
│       └── __init__.py  # Data models for the FastAPI application
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-ai-agent
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI application, execute the following command:

```
uvicorn src.main:app --reload
```

This will start the server at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

- **POST /check-misinformation**
  - Description: Checks the provided text for misinformation.
  - Request Body: JSON object containing the text to analyze.
  - Response: JSON object with the analysis results.

- **POST /check-ai-generated**
  - Description: Checks the provided text to determine if it is AI-generated.
  - Request Body: JSON object containing the text to analyze.
  - Response: JSON object with the analysis results.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.