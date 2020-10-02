# Discord Bot for toxic comment removal

**Disclaimer: the dataset for this competition contains text that may be considered profane, vulgar, or offensive.**

- Github : https://github.com/Sid200026/Discord-Bot-for-Toxic-Comment-Removal/
- Kaggle : https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/
- Discord : https://discordpy.readthedocs.io/en/latest/

---

### Table of Contents

- [ Introduction ](#introduction)
- [ Prerequisites](#prereq)
- [ Installation](#installation)
- [ Toxic Comment Classification](#toxic)
  - [ Using TFIDF](#tfidf)
  - [ Using Custom-Trained Embeddings](#custom)
- [ Team Members](#team)

---

<a name="introduction" />

### Introduction

Discussing things you care about can be difficult. The threat of abuse and harassment online means that many people stop expressing themselves and give up on seeking different opinions. Platforms struggle to effectively facilitate conversations, leading many communities to limit or completely shut down user comments. Toxic or insulting comments are no where more evident than the popular platform Discord since it is possible to remain anonymous on Discord. We try to develop a discord bot that can remove toxic comments, warn users, kick or ban them if required. It can also provide reports to the guild or server owner about all the members whoose comments have been deleted.

---

<a name="prereq" />

### Prerequisites

---

<a name="installation" />

### Installation

---

<a name="toxic" />

### Toxic Comment Classification

Given a sentence, classify it among the following labels

- toxic
- severe_toxic
- obscene
- threat
- insult
- identity_hate

<a name="tfidf" />

#### Using Term Frequency Inverse Document Frequency

- IPYNB File : [TFIDF and Logistic Regression](ML/Toxic_Comment_Classifier_tfidf.ipynb)

##### Output

<img src="https://github.com/Sid200026/Discord-Bot-for-Toxic-Comment-Removal/blob/master/ML/Output/Logistic%20Regression%20using%20TFIDF.png" alt="Output"/>

##### Steps

- Preprocessing

  - Convert to lowercase
  - Remove abbreviation, \n, double space, numeric, special characters. For example wont or won't will be converted into will not.
  - Remove url
  - Remove punctuations
  - Remove stop words like he, she, the, a etc
  - Lemmatization using WORDNET and POS Tagging

- Term Frequency Inverse Document Frequency
  - The TFIDF vector was trained on both the test and train data. The test and train dataset both consists of 1,50,000 rows. As a result, it will be very difficult for the tfidf vectorizer to provide a good result on unseen data. So we train this on the test data as well. Although this is wrong since test data shouldn't be used and it results in addition of bias, in a real world scenario the train dataset would contain enough input data so that our tfidf vectorizer can provide a good result even on unseen data.
- Logistic Regression and Multinomial Naive Bayes
  - Logistic Regression AUC-ROC : 0.98209
  - Multinomial Naive Bayers AUC-ROC : 0.95458
  - The parameters for the above two algorithms was tuned using GridSearchCV

##### Issues

- Since the dataset is large and running tfidf on a large dataset containing lot of text results in a huge datatable with numerous features. As a result it is very easy to run out of memory and face an error. I would recommend the usage of Google Colab or Kaggle Notebook to run the ipynb files.

<a name="custom" />

#### Using Custom-Trained Embeddings

- IPYNB File : [Custom-Trained Embedding](ML/Toxic_Comment_Classification_Custom_Word_Embedding.ipynb)
- Save files for Custom Embedding : https://drive.google.com/file/d/14CuMJxEADcO0EWM8x_TQh-QocuohmMnx/view?usp=sharing

##### Output

<img src="https://github.com/Sid200026/Discord-Bot-for-Toxic-Comment-Removal/blob/master/ML/Output/Custom%20Word%20Embedding.png" alt="Output"/>

##### Steps

- Preprocessing

  - Use Keras Tokenizer API to convert to lowercase, split the words according to tokens and remove punctuations

- Custom Word Embeddings using a Recurrent Neural Network ( LSTM ) trained on a GPU.
- AUC-ROC : 0.97

##### Issues

- The reason for a lower score as compared to logistic regression is the fact that the custom model used texts from the train set only. So the vocabulary size was small. As a result the model failed to provide an accurate embedding for words in the test set and thus resulting in a low score.

---

<a name="team" />

### Team Members

- Rajlaxmi Roy
- Siddharth Singha Roy
