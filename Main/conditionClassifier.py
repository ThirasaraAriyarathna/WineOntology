import json
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn import svm
import numpy as np
from nltk.stem.porter import PorterStemmer
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
    stemmer = PorterStemmer()

    def __init__(self):
        self.restoreClassifiers()

    def getDomainWords(self):
        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.domainWords[subject[0]] = results
        for key in self.domainWords:
            arr = []
            for dword in self.domainWords[key]:
                expanded_word = re.findall('[A-Z][^A-Z]*', dword)
                for word in expanded_word:
                    if word in ['Winery', 'Wine', 'Grape', 'Region']:
                        expanded_word.remove(word)
                arr.append(''.join(expanded_word))
            self.domainWords[key] = arr

    def createVocabulary(self):
        for intent in self.intents["intents"]:
            self.vocabulary[intent["label"]] = []
            keywords = self.domainWords[intent["label"]]
            for feature in intent["features"]:
                if "<" and ">" in feature:
                    for keyword in keywords:
                        self.vocabulary[intent["label"]].append(
                            re.sub('<' + intent["label"] + '>', keyword.lower(), feature))
                else:
                    self.vocabulary[intent["label"]].append(feature)


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

    def createTrainingSet(self):
        trainSet = {}
        for intent in self.intents['intents']:
            if intent['label'] == 'region':
                trainSet[intent['label']] = self.inputCleaning(self.vocabulary[intent["label"]])
            else:
                trainSet[intent['label']] = self.vocabulary[intent["label"]]
        # index = 0
        # for intent in self.intents["intents"]:
        #     trainSet.extend([[sent, index] for sent in self.inputCleaning(self.vocabulary[intent["label"]])])
        #     index += 1
        # trainSet = np.array(trainSet)
        return trainSet

    def createTestSet(self, classifier):
        testSet = []
        for intent in self.intents['intents']:
            if intent['label'] == classifier:
                output = int(-1)
            else:
                output = int(1)
            if intent['label'] == "region":
                sents = self.inputCleaning(self.vocabulary[intent["label"]])
            else:
                sents = self.vocabulary[intent["label"]]
            testSet.extend([[sent, output] for sent in sents])
        testSet = np.array(testSet)
        return testSet

    def trainer(self, classifier):

        trainSet = self.createTrainingSet()
        countVectorizer = CountVectorizer(ngram_range=(1, 1), token_pattern=r'\b\w+\b', min_df=1)
        xTrainCounts = countVectorizer.fit_transform(trainSet[classifier])
        clf = svm.OneClassSVM(nu=0.05, kernel="rbf", gamma=0.00004)
        clf.fit(xTrainCounts)
        vec_clf = Pipeline([('vectorizer', countVectorizer), ('clf', clf)])
        accuracy = self.accuracyCheck(classifier)
        filename = classifier + 'Classifier.sav'
        joblib.dump(vec_clf, "ModelData/" + filename)
        print accuracy
        # trainSet = self.createTrainingSet()
        # print trainSet
        # xTrain = list(trainSet[:, 0])
        # yTrain = list(trainSet[:, 1])
        # countVectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
        # xTrainCounts = countVectorizer.fit_transform(xTrain)
        # tfTransformer = TfidfTransformer()
        # xTrainTf = tfTransformer.fit_transform(xTrainCounts)
        # clf = svm.SVC(kernel='rbf', max_iter=-1)
        # x_train, x_test, y_train, y_test = train_test_split(xTrainTf, yTrain, test_size=0.3)
        # clf.fit(x_train, y_train)
        # predictions = clf.predict(x_test)
        # print accuracy_score(y_test, predictions)

    def conditionIndentifier(self, intent, inputChunks):

        intentClf = re.sub('about', '', intent).lower()
        conditions = {}
        for cls in self.intents['intents']:
            conditions[cls["label"]] = [0]
        for chunk in inputChunks:
            for cls in self.intents["intents"]:
                if intentClf != cls['label']:
                    clf = self.classifiers[cls["label"]]
                    if cls['label'] == 'region':
                        chunk = self.inputCleaning([chunk])[0]
                    result = clf.predict([chunk])
                    if result.astype(np.int64)[0] == -1:
                        conditions[cls["label"]][0] = 1
                        conditions[cls["label"]].append(chunk)
        print conditions
        return conditions

    def accuracyCheck(self, classifier):
        testSet = self.createTestSet(classifier)
        predictions = self.classifiers[classifier].predict(list(testSet[:, 0]))
        score = 0
        yTest = testSet[:, 1].astype(np.int64)
        predictions = predictions.astype(np.int64)
        for i in range(0, len(yTest)):
            if yTest[i] == predictions[i]:
                score +=1
        accuracy = score/float(predictions.size)
        print accuracy
        return accuracy
        # print predictions.size
        # inseders = predictions[predictions == -1].size
        # print inseders


    def restoreClassifiers(self):
        for intent in self.intents["intents"]:
            filename = intent["label"] + 'Classifier.sav'
            clf = joblib.load("ModelData/" + filename)
            self.classifiers[intent["label"]] = clf






# conditionClassifier = ConditionClassifier()
# conditionClassifier.getDomainWords()
# conditionClassifier.createVocabulary()
# conditionClassifier.trainer("region")
# conditionClassifier.accuracyCheck("region")
# cc = ConditionClassifier()
# cc.conditionIndentifier('aboutWine', ['australian wines'])



