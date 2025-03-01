import torch
import torch.nn.functional as F
from nltk.tokenize import sent_tokenize
from transformers import RobertaTokenizer

from src.ai_detector.preprocess import preprocess_text
from generated_text_detector.utils.model.roberta_classifier import RobertaClassifier


class GeneratedTextDetector:
    def __init__(self, 
                model_path: str = "SuperAnnotate/ai-detector", 
                max_len: int = 64, 
                preprocessing: bool = True) -> None:
        self.model = RobertaClassifier.from_pretrained(model_path)
        self.tokenizer = RobertaTokenizer.from_pretrained("SuperAnnotate/ai-detector")
        self.model.eval()
        self.max_len = max_len
        self.preprocessing = preprocessing
    
    def chunk_text(self, text: str) -> list[str]:
        if len(self.tokenizer.encode(text)) < self.max_len:
            return [text]
        chunks = []
        cur_chunk = ""
        cur_count_tokens = 0

        for sentence in sent_tokenize(text):
            temp_count_tokens = len(self.tokenizer.encode(sentence))
            if cur_count_tokens + temp_count_tokens > self.max_len:
                chunks.append(cur_chunk.strip())
                cur_chunk = sentence
                cur_count_tokens = temp_count_tokens
            else:
                cur_count_tokens += temp_count_tokens
                cur_chunk += " " + sentence
        chunks.append(cur_chunk.strip())

        return chunks

    def model_pass(self, texts: list[str]) -> list[float]:
        tokens = self.tokenizer.batch_encode_plus(
            texts,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='longest',
            truncation=True,
            return_token_type_ids=True,
            return_tensors="pt"
        )
        with torch.inference_mode():
            _, logits = self.model(**tokens)
        probas = F.sigmoid(logits).squeeze(1)
        
        return probas
    
    def detect(self, text: str) -> list[tuple[str, float]]:
        if self.preprocessing:
            text = preprocess_text(text)
        else:
            text = " ".join(text.split())

        text_chunks = self.chunk_text(text)
        scores = self.model_pass(text_chunks).tolist()
        res = list(zip(text_chunks, scores))
       
        return res
    
    def detect_report(self, text: str) -> dict:
        if self.preprocessing:
            text = preprocess_text(text)
        else:
            text = " ".join(text.split())

        text_chunks = self.chunk_text(text)
        scores = self.model_pass(text_chunks)

        gen_score = sum(scores) / len(scores)
        gen_score = gen_score.item() 

        res = {
            "generated_score": gen_score,
        }
       
        return res

