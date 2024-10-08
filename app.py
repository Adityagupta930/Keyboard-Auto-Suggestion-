# from flask import Flask, render_template, request
# import pandas as pd
# import textdistance
# import re
# from collections import Counter

# app = Flask(__name__)

# words = []

# with open('autocorrect book.txt', 'r', encoding='utf-8') as f:
#     data = f.read().lower()
#     words = re.findall('\w+', data)
#     words += words

# V = set(words)
# words_freq_dict = Counter(words)
# Total = sum(words_freq_dict.values())
# probs = {}

# for k in words_freq_dict.keys():
#     probs[k] = words_freq_dict[k] / Total

# @app.route('/')
# def index():
#     return render_template('index.html', suggestions=None)

# @app.route('/suggest', methods=['POST'])
# def suggest():
    
#     word = word.lower()
#     if word in V:
#         return('Your word seems to be correct', word)
#     else:
#         similarities = [1-(textdistance.Jaccard(qval=2).distance(v,word))  for v in words_freq_dict.keys()]
#         df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
#         df = df.rename(columns={'index':'Word',0:'Prob'})
#         df['Similarity'] = similarities
#         output = df.sort_values(['Similarity','Prob'],ascending=False).head(3)
#         return(output)


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
import textdistance
import re
from collections import Counter

app = Flask(__name__)

# Load and preprocess words from the book
words = []
with open('autocorrect book.txt', 'r', encoding='utf-8') as f:
    data = f.read().lower()
    words = re.findall(r'\w+', data)

V = set(words)  # Unique words
words_freq_dict = Counter(words)  # Word frequency
Total = sum(words_freq_dict.values())  # Total word frequency count

# Calculate probabilities for each word
probs = {}
for k in words_freq_dict.keys():
    probs[k] = words_freq_dict[k] / Total

@app.route('/')
def index():
    return render_template('index.html', suggestions=None)

@app.route('/suggest', methods=['POST'])
def suggest():
    # Get the word from the form
    word = request.form['keyword'].lower()  # Extract word from user input

    if word in V:
        return render_template('index.html', suggestions=[{'Word': word, 'Similarity': 1.0}])  # Exact match
    else:
        # Calculate Jaccard similarities for 2-grams
        jaccard = textdistance.Jaccard(qval=2)  # Jaccard distance with 2-grams
        similarities = [1 - jaccard.distance(v, word) for v in words_freq_dict.keys()]

        # Create a DataFrame with word probabilities and similarities
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index': 'Word', 0: 'Prob'})
        df['Similarity'] = similarities

        # Get the top 3 suggestions based on similarity and probability
        output = df.sort_values(['Similarity', 'Prob'], ascending=False).head(3)
        suggestions = output[['Word', 'Similarity']].to_dict('records')

        return render_template('index.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
