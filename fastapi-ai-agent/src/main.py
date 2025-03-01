import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from src.ai_detector.generated_text import GeneratedTextDetector
from src.fact_check.sources_cite import PerplexitySearchClient
from src.fact_check.search_utils import SearchEngine, FactChecker
from src.deepfake_model.roboflow import misinfo_detector_roboflow

load_dotenv()

# Initialize the search engine once at module level
search_engine = SearchEngine(cse=os.getenv("GOOGLE_CSE_ID"), api=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TextRequest(BaseModel):
    text: str

class FactRequest(BaseModel):
    fact: str

class ImageRequest(BaseModel):
    image_url: str
    
@app.post('/deep_fake_detection/')
async def deep_fake_detection(request: ImageRequest):
    try:
        # Initialize deepfake detector
        result = misinfo_detector_hf(request.image_url)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/deep_fake/")
async def deep_fake(request: ImageRequest):
    try:
        result = misinfo_detector_roboflow(request.image_url)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/check-ai-generated/")
async def check_ai_generated(request: TextRequest):
    try:

        if len(request.text) < 1000:
            string = request.text.split()
            string = request.text.split()
            if len(string) < 20:
                return {"generated_score": -1}

        detector = GeneratedTextDetector()
        result = detector.detect_report(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_fact_checker():
    # Use the existing search engine and create a fact checker
    checker = FactChecker(llm_api=os.getenv("OPENAI_API_KEY"), search_engine=search_engine)
    return checker

@app.get("/fact-check/status/")
async def get_fact_check_status():
    return {
        "status": "OK"
    }

@app.post("/get_links/")
async def get_links(request: TextRequest):
    try:
        client = PerplexitySearchClient(api_key=os.getenv("PERPLEXITY_API_KEY"))
        result = client.search(request.text, num_sources=3)
        print(result)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/fact-check/")
async def check_fact(request: FactRequest, fact_checker: FactChecker = Depends(get_fact_checker)):
    try:
        result = fact_checker.fact_check(request.fact)
        return {"result": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
