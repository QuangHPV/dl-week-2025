from pydantic import BaseModel
from transformers import pipeline


from generated_text_detector.utils.model.roberta_classifier import RobertaClassifier
from generated_text_detector.utils.preprocessing import preprocessing_text
from transformers import AutoTokenizer
import torch.nn.functional as F

model_ai_detect = RobertaClassifier.from_pretrained("SuperAnnotate/ai-detector")
tokenizer_ai_detect = AutoTokenizer.from_pretrained("SuperAnnotate/ai-detector")
model_ai_detect.eval()

def ai_text_detector(text: str):
    text = preprocessing_text(text)
    tokens = tokenizer_ai_detect.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        padding='longest',
        truncation=True,
        return_token_type_ids=True,
        return_tensors="pt"
    )
    _, logits = model_ai_detect(**tokens)
    proba = F.sigmoid(logits).squeeze(1).item()
    return proba > 0.5


# misinfo_detector = ###
# ai_text_detector = ###

# Define request and response models
class TextRequest(BaseModel):
    text: str

class DetectionResponse(BaseModel):
    is_misinformation: bool
    is_ai_generated: bool
    misinfo_label: str
    ai_generated_label: str