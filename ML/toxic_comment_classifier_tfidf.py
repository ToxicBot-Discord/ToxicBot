# -*- coding: utf-8 -*-
"""Toxic Comment Classifier TFIDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dRvXLOSmEwfRRIctLiTROt4-UVGxbXtk

# Toxic Comment Classification
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from scipy.sparse import hstack
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
from  spacy.lang.en.stop_words import STOP_WORDS

import re
import string
import gc
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

useLogisticRegression = True
useNaiveBayes = False

df = pd.read_csv('train.csv')
df.head()

df.dtypes

df = df.drop(columns='id')
df.head()

categories = df.columns[1:]
categories

test_data = pd.read_csv('test.csv')
test_data.head()

ids = test_data.iloc[:,0]
test_data = test_data.drop(columns='id')
ids

test_data.head()

"""# Preprocessing"""

def to_lower(text):
  return text.lower()

def remove_abbreviation(text):
    text = re.sub("^ *","", text)
    text = re.sub("\n"," ",text)
    text = re.sub(' {2,}', ' ', text)
    text = re.sub("\[.*\]"," ",text)
    text = re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"," ",text)
    text = re.sub(r"\?"," ",text)
    text = re.sub("don'?t","do not",text)
    text = re.sub("doesn'?t", "does not",text)
    text = re.sub("didn'?t", "did not",text)
    text = re.sub("hasn'?t", "has not",text)
    text = re.sub("haven'?t", "have not",text)
    text = re.sub("hadn'?t", "had not",text)
    text = re.sub("won'?t", "will not",text)
    text = re.sub("wouldn'?t", "would not",text)
    text = re.sub("can'?t", "can not",text)
    text = re.sub("cannot", "can not",text)
    text = re.sub("i'?m", "i am",text)
    text = re.sub("i'?ll", "i will",text)
    text = re.sub("it'?s", "it is",text)
    text = re.sub("that'?s", "that is",text)
    text = re.sub("weren'?t", "were not",text)
    text = re.sub("i'?d","i would",text)
    text = re.sub("i'?ve","i have",text)
    text = re.sub("she'?d","she would",text)
    text = re.sub("they'?ll","they will",text)
    text = re.sub("they'?re","they are",text)
    text = re.sub("we'?d","we would",text)
    text = re.sub("we'?ll","we will",text)
    text = re.sub("we'?ve","we have",text)
    text = re.sub("it'?ll","it will",text)
    text = re.sub("there'?s","there is",text)
    text = re.sub("where'?s","where is",text)
    text = re.sub("they'?re","they are",text)
    text = re.sub("let'?s","let us",text)
    text = re.sub("couldn'?t","could not",text)
    text = re.sub("shouldn'?t","should not",text)
    text = re.sub("wasn'?t","was not",text)
    text = re.sub("could'?ve","could have",text)
    text = re.sub("might'?ve","might have",text)
    text = re.sub("must'?ve","must have",text)
    text = re.sub("should'?ve","should have",text)
    text = re.sub("would'?ve","would have",text)
    text = re.sub("who'?s","who is",text)
    text = re.sub("you'?re", "you are", text)
    text = re.sub("y'?all", "you all", text)
    text = re.sub("'d've"," would have", text)
    text = re.sub("'d"," would", text)
    text = re.sub("'re"," are", text)
    text = re.sub("'ve"," have", text)
    text = re.sub("\bim\b", "i am",text)
    text = re.sub(r'[^\w\s]','',text)
    text = re.sub("[^a-zA-Z ]+", "", text)
    return text

def remove_url(text):
  text = re.sub(r"\b(?:(?:https|ftp|http|www)://)?\w[\w-]*(?:\.[\w-]+)+\S*", '', text, flags=re.MULTILINE)
  return text

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

stopwords = list(STOP_WORDS)

def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in stopwords])

def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    text_arr = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in word_tokenize(text)]
    return " ".join(text_arr)

def preprocessing_pipeline(text):
  text = to_lower(text)
  text = remove_url(text)
  text = remove_punctuation(text)
  text = remove_abbreviation(text)
  text = remove_stopwords(text)
  text = lemmatize(text)
  return text

df['comment_text'] = df.loc[:,'comment_text'].apply(lambda text : preprocessing_pipeline(text))

test_data['comment_text'] = test_data.loc[:,'comment_text'].apply(lambda text : preprocessing_pipeline(text))

df.to_csv('processed_train.csv', index=False)
test_data.to_csv('processed_test.csv', index=False)

del remove_abbreviation
del to_lower
del remove_punctuation
del remove_stopwords
del remove_url
del get_wordnet_pos
del lemmatize
del preprocessing_pipeline

del PUNCT_TO_REMOVE
del stopwords

gc.collect()

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from scipy.sparse import hstack
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
from  spacy.lang.en.stop_words import STOP_WORDS

import re
import string
import gc
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('processed_train.csv', dtype={'comment_text':'string'})
df.head()

test_data = pd.read_csv('processed_test.csv', dtype={'comment_text':'string'}).fillna('')
test_data.head()

categories = df.columns[1:]
categories

df.dtypes

df.isna().sum()

df = df.dropna()

test_data.isna().sum()

"""# Text to Numeric Conversion"""

all_data = pd.concat([df, test_data])
all_data.head()

all_data.shape

X = all_data.iloc[:,0].values
X.shape

X_train = df.iloc[:,0].values
X_train.shape

X_test = test_data.iloc[:,0].values
X_test.shape

X.dtype

y_train = df.iloc[:,1:].values
y_train.shape

del df
del test_data
del all_data

gc.collect()

word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    ngram_range=(1, 2),
    max_features=10000,
    dtype=np.float32,
    lowercase=False
)

word_vectorizer.fit(X)

X_train_word = word_vectorizer.transform(X_train)

X_test_word = word_vectorizer.transform(X_test)

X_train_word.shape

X_test_word.shape

char_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='char',
    ngram_range=(2, 6),
    max_features=20000,
    lowercase=False,
    dtype=np.float32)

char_vectorizer.fit(X)

X_train_char = char_vectorizer.transform(X_train)

X_test_char = char_vectorizer.transform(X_test)

X_train_char.shape

X_test_char.shape

X_train = hstack([X_train_word, X_train_char,])
X_test = hstack([X_test_word, X_test_char])

del X_train_char
del X_test_char
del X_test_word
del X_train_word

del X

del char_vectorizer
del word_vectorizer

gc.collect()

"""# Logistic Regression"""

result = pd.DataFrame()
result.head()

scores = 0

param_grid = {
    'C' : np.arange(0.1,1.1,0.1)
}

C_values = [1, 0.4, 0.8, 0.9, 0.7000000000000001, 0.8]

for index,category in enumerate(categories):
    logistic_regression = LogisticRegression(C=C_values[index], solver='sag')
    # clf = GridSearchCV(logistic_regression, param_grid = param_grid, cv = 3, n_jobs=-1, scoring='roc_auc')
    # clf.fit(X_train, y_train[:,index])
    # print(clf.best_params_)
    score = np.mean(cross_val_score(logistic_regression, X_train, y_train[:,index], cv=3, scoring='roc_auc'))
    scores += score
    if useLogisticRegression:
        logistic_regression.fit(X_train, y_train[:,index])
        y_pred = logistic_regression.predict_proba(X_test)
        result[f'{category}'] = y_pred[:, 1]
    print(f"{category} : {score}")

print("\nAverage Score : {:.5f}".format(scores/6))

result.head()

"""# Multinomial Naive Bayes"""

scores = 0

param_grid = {
    'alpha' : np.arange(0.1,1.5,0.15)
}

alpha_values = [0.9999999999999999, 0.25, 0.85, 0.1, 0.7, 0.25]

for index,category in enumerate(categories):
    multinomial_nb = MultinomialNB()
    # clf = GridSearchCV(multinomial_nb, param_grid = param_grid, cv = 3, n_jobs=-1, scoring='roc_auc')
    # clf.fit(X_train, y_train[:,index])
    # print(clf.best_params_)
    score = np.mean(cross_val_score(multinomial_nb, X_train, y_train[:,index], cv=3, scoring='roc_auc'))
    scores += score
    print(f"{category} : {score}")

print("\nAverage Score : {:.5f}".format(scores/6))

"""# Kaggle Submission"""

!pip install kaggle

from google.colab import files
files.upload()

! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

result.insert(0, 'id', ids)
result.head()

result.shape

result.to_csv('submission.csv', index=False)

! kaggle competitions submit -c jigsaw-toxic-comment-classification-challenge -f submission.csv -m "Second Submission"