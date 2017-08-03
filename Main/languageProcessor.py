import re
import nltk
import json
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class LanguageProcessor():

    forest = RandomForestClassifier(n_estimators=100)
    with open('intents.json') as json_data:
        intents = json.load(json_data)
    stemmer = LancasterStemmer()
    vocabulary = []
    classes = []
    documents = []
    ignore_words = ['?', '.', '!']

    def trainer(self):

        training = []

        for doc in self.documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [self.stemmer.stem(word.lower()) for word in pattern_words]
            for w in self.vocabulary:
                bag.append(1) if w in pattern_words else bag.append(0)
            training.append([bag, self.classes.index(doc[1])])

        training = np.array(training)

        x = list(training[:, 0])
        y = list(training[:, 1])

        # training model
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
        self.forest.fit(x_train, y_train)
        predictions = self.forest.predict(x_test)
        print accuracy_score(y_test, predictions)

    def intentIdentifier(self, inputString):

        stemmedWords = self.tokenizer(inputString)

        bag = []
        for i in self.vocabulary:
            if i in stemmedWords:
                bag.append(1)
            else:
                bag.append(0)
        predictedClass = self.forest.predict(bag)
        if len(predictedClass) > 0:
            print self.classes[predictedClass[0]]
            return self.classes[predictedClass[0]]
        else:
            return ""


    def createVocabulary(self, domainWords):

        for intent in self.intents['intents']:
            for domainWord in domainWords[intent['label']]:
                d = re.findall('[A-Z][^A-Z]*', domainWord)
                for pattern in intent['requests']:
                    w = nltk.word_tokenize(pattern)
                    w.extend(d)
                    self.vocabulary.extend(w)
                    self.documents.append((w, intent['label']))
                    if intent['label'] not in self.classes:
                        self.classes.append(intent['label'])
        self.vocabulary = [self.stemmer.stem(w.lower()) for w in self.vocabulary if w not in self.ignore_words]
        self.vocabulary = sorted(list(set(self.vocabulary)))
        self.classes = sorted(list(set(self.classes)))

    def tokenizer(self, inputString):

        # not necessary for this stage as the assumption is user inputs only one sentence.
        # If more than one need to modify the code
        inputSentences = nltk.sent_tokenize(inputString)
        inputWords = [nltk.word_tokenize(sentence) for sentence in inputSentences]
        flattenedWords = [y for x in inputWords for y in x]
        stemmedWords = [self.stemmer.stem(word.lower()) for word in flattenedWords]
        return stemmedWords

    def getIntents(self):

        arr = []
        for intent in self.intents['intents']:
            arr.append(intent['label'])
        return arr

    def entityExtractor(self, inputString, keywords):

        entities = []
        inputWords = nltk.word_tokenize(inputString)
        for word in inputWords:
            x = word.lower()
            if x in keywords:
                entities.append(word)
        return entities


