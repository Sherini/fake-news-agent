import pandas as pd
from datasets import Dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import Trainer, TrainingArguments

# Load dataset
df = pd.read_csv("dataset/news.csv")

# Convert to HuggingFace dataset
dataset = Dataset.from_pandas(df)

# Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(example):
    return tokenizer(example['text'], truncation=True, padding='max_length')

dataset = dataset.map(tokenize, batched=True)

# Train-test split
dataset = dataset.train_test_split(test_size=0.2)

# Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

# SAFE training settings
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,   # VERY IMPORTANT (safe)
    per_device_train_batch_size=4,   # small batch
    per_device_eval_batch_size=4,
    logging_steps=10,
    save_strategy="no"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test']
)

# Train
trainer.train()

# Save model
model.save_pretrained("models/distilbert_fake_news")
tokenizer.save_pretrained("models/distilbert_fake_news")

print("✅ Training completed & model saved!")