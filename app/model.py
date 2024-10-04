import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class ToxicityModel:
    def __init__(self, model_name='sismetanin/rubert-toxic-pikabu-2ch', save_directory='toxicity_model'):
        self.save_directory = save_directory
        self.model_name = model_name

        # Проверяем, существует ли сохранённая модель
        if os.path.exists(save_directory):
            self.tokenizer = AutoTokenizer.from_pretrained(save_directory)
            self.model = AutoModelForSequenceClassification.from_pretrained(save_directory)
            print("Модель загружена из сохранённой директории.")
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.save_model(save_directory)
            print("Модель загружена и сохранена.")

    def save_model(self, save_directory):
        os.makedirs(save_directory, exist_ok=True)
        self.tokenizer.save_pretrained(save_directory)
        self.model.save_pretrained(save_directory)
        print(f"Модель сохранена в {save_directory}.")

    def predict_toxicity(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        toxicity_score = probabilities[0][1].item()  # Вероятность токсичности
        return toxicity_score
