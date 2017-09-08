import nltk
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class Trainer():

    classifier = any()
    with open('intents.json') as json_data:
        intents = json.load(json_data)
    stemmer = nltk.stem.LancasterStemmer()
    vocabulary = []
    classes = []
    documents = []
    ignore_words = ['?', '.', '!']

    def randomForestTrainer(self):

        self.classifier = RandomForestClassifier(n_estimators=100)
        trainingSet = self.createTrainingSet()
        x = trainingSet[0]
        y = trainingSet[1]
        # training model
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
        self.forest.fit(x_train, y_train)
        predictions = self.forest.predict(x_test)
        return accuracy_score(y_test, predictions)

    def createVocabulary(self):

        for intent in self.intents['intents']:
            for pattern in intent['requests']:
                w = nltk.word_tokenize(pattern)
                self.vocabulary.extend(w)
                self.documents.append((w, intent['label']))
                if intent['label'] not in self.classes:
                    self.classes.append(intent['label'])

        self.vocabulary = [self.stemmer.stem(w.lower()) for w in self.vocabulary if w not in self.ignore_words]
        self.vocabulary = sorted(list(set(self.vocabulary)))
        self.classes = sorted(list(set(self.classes)))

    def createTrainingSet(self):

        self.createVocabulary()
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
        return x, y


threshold = raw_input("Enter the threshold accuracy (between 0 and 1)")
accuracy = 0
trainer = Trainer()
while accuracy < threshold:
    accuracy = trainer.randomForestTrainer()
