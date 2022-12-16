from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
from data_utils import EmotionDetectionDataset

app = Flask(__name__)

# Instantiate model, load Tokenizer and Config
tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1') # load pre-trained tokenizer from indobert in huggingface
config = BertConfig.from_pretrained('azizp128/bert-emotion-prediction') # load pre-trained config from azizp128 in huggingface
model = BertForSequenceClassification.from_pretrained('azizp128/bert-emotion-prediction', config=config)

# load emotion labels
w2i, i2w = EmotionDetectionDataset.LABEL2INDEX, EmotionDetectionDataset.INDEX2LABEL

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def predict():
    text = request.form.get('user_input')
    subwords = tokenizer.encode(text)
    subwords = torch.LongTensor(subwords).view(1, -1).to(model.device)

    logits = model(subwords)[0]
    label = torch.topk(logits, k=1, dim=-1)[1].squeeze().item()

    output = i2w[label]

    return render_template('index.html', output_text=output)


if __name__ == "__main__":
    app.run(debug=True)