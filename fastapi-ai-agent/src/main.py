from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.generated_text import GeneratedTextDetector
# from src.agent import misinfo_detector

app = FastAPI()

class TextRequest(BaseModel):
    text: str

# @app.post("/check-misinformation/")
# async def check_misinformation(request: TextRequest):
#     try:
#         result = misinfo_detector(request.text)
#         return {"result": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-ai-generated/")
async def check_ai_generated(request: TextRequest):
    try:
        detector = GeneratedTextDetector()
        result = detector.detect_report(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)