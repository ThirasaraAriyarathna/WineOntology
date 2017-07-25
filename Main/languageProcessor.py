import re
import nltk
import json
import numpy as np
import tensorflow as tf
import tflearn
from tensorflow.contrib import learn
from nltk.stem.lancaster import LancasterStemmer
from sklearn.ensemble import RandomForestClassifier

stemmer = LancasterStemmer()

with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []
classes = []
documents = []
ignore_words = ['?', '.', '!']

for intent in intents['intents']:
    for pattern in intent['requests']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['label']))
        if intent['label'] not in classes:
            classes.append(intent['label'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# training data for tf

training = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    bag = []

    pattern_words = doc[0]

    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
# random.shuffle(training)

training = np.array(training)

xTrain = list(training[:, 0])
yTrain = list(training[:, 1])

forest = RandomForestClassifier(n_estimators=100)
forest.fit(xTrain, yTrain)


def intentIdentifier(inputString):

    processedWords = tokenizer(inputString)

    bag = []
    for i in words:
        if i in processedWords:
            bag.append(1)
        else:
            bag.append(0)

    print processedWords
    print words
    print classes
    print documents
    print xTrain
    print yTrain
    print classes
    print
    predictedClass = forest.predict(bag)
    print predictedClass[0]


def tokenizer(inputString):

    # not necessary for this stage as the assumption is user inputs only one sentence.
    # If more than one need to modify the code
    inputSentences = nltk.sent_tokenize(inputString)
    inputWords = [nltk.word_tokenize(sentence) for sentence in inputSentences]
    z = [y for x in inputWords for y in x]

    stemmedWords = [stemmer.stem(word.lower()) for word in z]
    print inputString
    print inputSentences
    print inputWords
    print z
    return stemmedWords