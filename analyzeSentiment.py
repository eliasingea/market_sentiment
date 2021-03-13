from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import urllib
import csv
from scipy.special import softmax
import numpy as np



task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)

def create_labels():
  labels=[]
  mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/mapping.txt"
  with urllib.request.urlopen(mapping_link) as f:
      html = f.read().decode('utf-8').split("\n")
      csvreader = csv.reader(html, delimiter='\t')
  labels = [row[1] for row in csvreader if len(row) > 1]
  return labels

def returnSentiment(text):
  encoded_input = tokenizer(text, return_tensors='tf')
  print("encoded_input")
  output = model(encoded_input)
  scores = output[0][0].numpy()
  scores = softmax(scores)

  ranking = np.argsort(scores)
  ranking = ranking[::-1]
  return_var = {}
  labels = create_labels()
  for i in range(scores.shape[0]):
      l = labels[ranking[i]]
      s = scores[ranking[i]]
      return_var[l] = np.round(float(s), 4)

  return return_var


text = "This is a positive tweet :)"
returnSentiment(text)