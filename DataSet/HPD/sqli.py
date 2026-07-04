import pandas as pd
import re

file_path = 'sqli.xlsx'
df = pd.read_excel(file_path)

sentences = df['payload'].tolist()


def preprocess_sentence(sentence):
    if isinstance(sentence, str):
        sentence = sentence.replace('+', ' ')
        return sentence.strip()
    else:
        return None


unique_sentences = set()
for sentence in sentences:
    processed_sentence = preprocess_sentence(sentence)
    if processed_sentence is not None:
        unique_sentences.add(processed_sentence)

output_file = 'sqli.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for sentence in unique_sentences:
        f.write(str(sentence) + '\n')

print(f"Unique and preprocessed sentences have been written to {output_file}")
