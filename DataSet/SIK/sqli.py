import pandas as pd

file_path = 'sqli.xlsx'
df = pd.read_excel(file_path)

sentences = df['Sentence'].tolist()

unique_sentences = set()
for sentence in sentences:
    unique_sentences.add(str(sentence))

output_file = 'sqli.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for sentence in unique_sentences:
        f.write(sentence + '\n')

print(f"Unique and preprocessed sentences have been written to {output_file}")
