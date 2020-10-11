# ToxicBot

<img src="https://github.com/Sid200026/ToxicBot/blob/master/public/Logo.png" alt="Toxic Bot">

**Disclaimer: the dataset for this competition contains text that may be considered profane, vulgar, or offensive.**

- Github : https://github.com/Sid200026/ToxicBot/
- Discord : https://discord.com/

**View the demo of ToxicBot on Youtube👇👇**

<a href="https://www.youtube.com/watch?v=a3jQCigncSs"><img width="500" src="https://i.imgur.com/4whsJOt.png"></img></a>

### Table of Contents

- [ Introduction ](#introduction)
- [ Prerequisites](#prereq)
- [ Installation](#installation)
- [ Toxic Comment Classification](#toxic)

---

<a name="introduction" />

### Introduction

Discussing things you care about can be difficult. The threat of abuse and harassment online means that many people stop expressing themselves and give up on seeking different opinions. Platforms struggle to effectively facilitate conversations, leading many communities to limit or completely shut down user comments. Toxic or insulting comments are no where more evident than the popular platform Discord since it is possible to remain anonymous on Discord. We try to develop a discord bot that can remove toxic comments and warn users. It can also provide reports to the guild or server owner about all the members whoose comments have been deleted ( not implemented ).

---

<a name="prereq" />

### Prerequisites

- python 3.6+
- pip
- Discord Developer Account

---

<a name="installation" />

### Installation - Mac/Linux

```bash
apple@Apples-MacBook-Air ~ % git clone https://github.com/Sid200026/ToxicBot.git
apple@Apples-MacBook-Air ~ % cd ToxicBot
apple@Apples-MacBook-Air ~ % bash setup.sh
apple@Apples-MacBook-Air ~ % cd ToxicBot
apple@Apples-MacBook-Air ~ % source env/bin/activate
apple@Apples-MacBook-Air ~ % python app.py
```
### Installation - Windows

* Download and Install Python 3.6 (64 Bit Version)
  https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe
* Download and Install git for windows from https://git-scm.com/download/win 
* Now open the "git bash" app (Righ-Click on the desktop you will find the "git bash here" option.)
* Clone the repository -
```
git clone https://github.com/Sid200026/ToxicBot.git
```
* Execute these commands in your git bash
```
cd ToxicBot
sh setup-win.sh
```
* When you exceute the ``` sh setup-win.sh ``` after sometime, it will ask you for discord token. Paste your token and hit enter.
* installation Done -
  Now we have to run the app
* To run execute the following commands in your git bash
```
cd ToxicBot
. env/Scripts/activate
python app.py
```
---

<a name="toxic" />

### Toxic Comment Classification

#### Model 1
- Github : https://github.com/Sid200026/Toxic-Comment-Classification
- Kaggle : https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/
- Algorithm : GloVe Embedding and Recurrent Neural Network ( LSTM )

#### Model 2 ( Used here )
- Github : https://github.com/Sid200026/Unintended-Bias-in-Toxicity-Classification
- Kaggle : https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification
- Algorithm : GloVe Embedding and Recurrent Neural Network ( LSTM )

---
