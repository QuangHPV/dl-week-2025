import requests
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PerplexitySearchClient:
    def __init__(self, api_key: str, model: str = "sonar"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def search(self, query: str, num_sources: int = 5, 
               additional_instructions: Optional[str] = None):
        system_prompt = (
            f"Search the web for information about: {query}. "
            f"Provide {num_sources} sources from credible publications, academic journals, "
            "or recognized authorities on the subject. "
            "For each source, extract the title, write a concise summary (1-2 sentences), and include the link."

        )
        
        if additional_instructions:
            system_prompt += f" {additional_instructions}"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
        }
        
        return self._make_request(payload)
    
    def custom_search(self, query: str, system_prompt: str, 
                      response_model: BaseModel) -> Any:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
        }
        
        return self._make_request(payload, response_model)
    
    def _make_request(self, payload: Dict[str, Any], 
                     response_model: Optional[BaseModel] = None) -> Any:
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return content[8:-4]
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            raise
        except Exception as e:
            print(f"Error processing results: {e}")
            raise