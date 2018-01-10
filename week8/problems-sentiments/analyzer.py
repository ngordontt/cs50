import nltk
from nltk.tokenize import TweetTokenizer

pos_var = []
neg_var = []

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.p = positives
        self.n = negatives

        #use with tot open file as it also close file at end
        with open(positives, 'r') as pos_tx:
            for line in pos_tx:
                #check each read line, only lines without ; or \n are added to list
                if not (line.startswith(";") or line.startswith('\n')):
                    pos_var.append(line.strip())
            #makes list tuple for faster searching, choose tuple as there were no key pairs
            tuple(pos_var)

        with open(negatives, 'r') as neg_tx:
            for line in neg_tx:
                if not (line.startswith(";") or line.startswith('\n')):
                    neg_var.append(line.strip())
            tuple(neg_var)

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        self.text = text
        total = 0
        #splits the supplied text
        tokens = nltk.word_tokenize(self.text)

        #loop thur list and assigns value, returning total value
        for wrd in tokens:
            if wrd.lower() in pos_var:
                total += 1
            elif wrd.lower() in neg_var:
                total -= 1

        return total

    def analyze_tweet(self, text):
        """Analyze text for sentiment, returning its score."""
        self.text = text
        total = 0
        #splits the supplied text
        tknzr = nltk.tokenize.TweetTokenizer(preserve_case=False, strip_handles=True)
        tokens = tknzr.tokenize(text)

        #loop thur list and assigns value, returning total value
        for wrd in tokens:
            if wrd.lower() in pos_var:
                total += 1
            elif wrd.lower() in neg_var:
                total -= 1

        return total