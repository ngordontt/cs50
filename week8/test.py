import os
import sys
import nltk

positives_var = []
negatives_var = []
twt_var = []
score = 0

positives = os.path.join(sys.path[0], "positive-words.txt")
negatives = os.path.join(sys.path[0], "negative-words.txt")
text = os.path.join(sys.path[0], "Pres_twt.txt")

with open(positives, 'r') as pos_tx:
    for line in pos_tx:
        if not (line.startswith(";") or line.startswith('\n')):
            positives_var.append(line.strip())
        tuple(positives_var)

with open(negatives, 'r') as neg_tx:
    for line in neg_tx:
        if not (line.startswith(";") or line.startswith('\n')):
            negatives_var.append(line.strip())
        tuple(negatives_var)

with open(text, 'r') as twt_tx:
    for line in twt_tx:
       twt_var.append(line.strip())
    tuple(twt_var)

tokens = nltk.word_tokenize(twt_var)

#print(twt_var)

for wrd in tokens:
    if wrd in positives_var:
        score += 1
    elif wrd in negatives_var:
        score -= 1

print(score)