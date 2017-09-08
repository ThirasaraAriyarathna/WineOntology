import json
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
from queryGenerator import QueryGenerator
from chunker import Chuncker
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
import string
import nltk

class ConditionClassifier:

    with open('intents2.json') as json_data:
        intents = json.load(json_data)
    domainWords = {}
    vocabulary = {}
    subjects = [("sugar", "WineSugar"), ("flavor", "WineFlavor"), ("maker", "Winery"), ("region", "Region"),
                ("color", "WineColor"), ("grape", "WineGrape"), ("body", "WineBody"), ("wine", "hasMaker")]
    classifiers = {}
    queryGenerator = QueryGenerator()
    stemmer = LancasterStemmer()

    def __init__(self):
        self.restoreClassifiers()
        # pass

    def getDomainWords(self):
        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.domainWords[subject[0]] = results

    def createVocabulary(self):
        for intent in self.intents["intents"]:
            self.vocabulary[intent["label"]] = []
            keywords = self.domainWords[intent["label"]]
            for feature in intent["features"]:
                for keyword in keywords:
                    self.vocabulary[intent["label"]].append(re.sub('<' + intent["label"] + '>', keyword.lower(), feature))

    def inputCleaning(self, inputArray):
        # sent = input
        # arr = [char for char in sent if char not in string.punctuation]
        # noPunc = ''.join(arr)
        outputArray = []
        for sent in inputArray:
            tokanizedWords = nltk.word_tokenize(sent)
            stemmedWords = [self.stemmer.stem(word.lower()) for word in tokanizedWords]
            stemmedSent = ' '.join(stemmedWords)
            outputArray.append(stemmedSent)
        return outputArray

    def trainer(self):
        # training = {}
        # for intent in self.intents["intents"]:
        #     training[intent['label']] = self.inputCleaning(self.vocabulary[intent["label"]])
        trainingSet = []
        for intent in self.intents["intents"]:
            trainingSet.extend(self.vocabulary[intent["label"]])
        # print trainingSet
        # tfVectorizer = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
        # tfVectorizer.fit(trainingSet)
        for intent in self.intents["intents"]:
            countVectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
            xTrainCounts = countVectorizer.fit_transform(self.vocabulary[intent["label"]])
            clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
            # xTrainTf = tfVectorizer.transform(self.vocabulary[intent['label']])
            clf.fit(xTrainCounts)
            vec_clf = Pipeline([('vectorizer', countVectorizer), ('clf', clf)])
            filename = intent["label"] + 'Classifier.sav'
            joblib.dump(vec_clf, "ModelData/" + filename)

    def conditionIndentifier(self, inputChunks):
        conditions = {}
        # for chunk in inputChunks:
        for intent in self.intents["intents"]:
            # if intent['label'] != inputIntent:
            clf = self.classifiers[intent["label"]]
            result = clf.predict([inputChunks])
            print result
            if result.astype(np.int64)[0] == 1:
                conditions[intent["label"]] = [1, ""]

        print conditions
        return conditions

    def restoreClassifiers(self):
        for intent in self.intents["intents"]:
            filename = intent["label"] + 'Classifier.sav'
            clf = joblib.load("ModelData/" + filename)
            self.classifiers[intent["label"]] = clf




# conditionClassifier = ConditionClassifier()
# conditionClassifier.getDomainWords()
# conditionClassifier.createVocabulary()
# print conditionClassifier.vocabulary
# conditionClassifier.trainer()
cc = ConditionClassifier()
cc.conditionIndentifier("what are the red wines")




