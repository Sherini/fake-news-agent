from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained("models/distilbert_fake_news")
model = AutoModelForSequenceClassification.from_pretrained("models/distilbert_fake_news")

def predict_dl(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)

    prediction = torch.argmax(probs).item()
    confidence = probs[0][prediction].item()

    result = "Real News" if prediction == 1 else "Fake News"

    return result, confidence