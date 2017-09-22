import json
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import numpy as np
from nltk.stem.porter import PorterStemmer
import nltk
from queryGenerator import QueryGenerator
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
import string
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class IntentClassifier:

    with open('intents1.json') as json_data:
        intents = json.load(json_data)
    domainWords = {}
    vocabulary = {}
    subjects = [("region", "Region"), ("sugar", "WineSugar"), ("flavor", "WineFlavor"), ("maker", "Winery"),
                ("color", "WineColor"), ("grape", "WineGrape"), ("body", "WineBody"), ("wine", "hasMaker")]
    queryGenerator = QueryGenerator()
    stemmer = PorterStemmer()

    def __init__(self):
        self.classifiers = self.restoreClassifiers()


    def getDomainWords(self):
        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.domainWords[subject[0]] = results

    def createVocabulary(self):
        for intent in self.intents["intents"]:
            self.vocabulary[intent["label"]] = []
            for feature in intent["features"]:
                subject = re.sub('about', '', intent["label"]).lower()
                keywords = self.domainWords[subject]
                if "<" and ">" in feature:
                    for keyword in keywords:
                        self.vocabulary[intent["label"]].append(re.sub('<' + subject + '>', keyword.lower(), feature))
                else:
                    self.vocabulary[intent["label"]].append(feature)

    def inputProcessing(self, input, isTrain):
        arr = [char for char in input if char not in string.punctuation]
        noPunc = ''.join(arr)
        tokanizedWords = nltk.word_tokenize(noPunc)
        stemmedWords = [self.stemmer.stem(word.lower()) for word in tokanizedWords]
        if isTrain:
            stemmedSent = ' '.join(stemmedWords)
        else:
            if len(stemmedWords) < 20:
                stemmedSent = ' '.join(stemmedWords)
            else:
                stemmedSent = ' '.join(stemmedWords[:20])
        return stemmedSent


    def createTrainingSet(self):
        # trainSet = []
        # index = 0
        # for intent in self.intents["intents"]:
        #     for sent in self.vocabulary[intent["label"]]:
        #         processedInput = self.inputProcessing(sent, True)
        #         trainSet.append([processedInput, index])
        #     index +=1
        # trainSet = np.array(trainSet)
        # return trainSet

        trainSet = {}
        for intent in self.intents["intents"]:
            trainSet[intent['label']] = []
            for sent in self.vocabulary[intent["label"]]:
                processedInput = self.inputProcessing(sent, True)
                trainSet[intent['label']].append(processedInput)
        return trainSet

    def createTestSet(self, classifier):
        testSet = []
        for intent in self.intents['intents']:
            if intent['label'] == classifier:
                output = int(-1)
            else:
                output = int(1)
            testSet.extend([[self.inputProcessing(sent, False), output] for sent in self.vocabulary[intent["label"]]])
        testSet = np.array(testSet)
        return testSet

    def trainer(self, classifier):
        inputs = self.createTrainingSet()
        train_set = []
        for key in inputs:
            train_set.extend(inputs[key])
        countVectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
        train_counts = countVectorizer.fit_transform(inputs[classifier])
        print countVectorizer.vocabulary_
        # tfTransformer = TfidfTransformer(smooth_idf=True, norm='l2')
        # tfTransformer.fit(train_counts)
        x_train_counts = countVectorizer.transform(inputs[classifier])
        # x_train_tf = tfTransformer.transform(x_train_counts)
        # print len(np.array(x_train_counts.todense()[0])[0].tolist())
        # for i in range(0, len(x_train_counts.todense())):
        #     for j in range(0, len(np.array(x_train_counts.todense()[i])[0].tolist())):
        #         if np.array(x_train_counts.todense()[i])[0].tolist()[j] == 1:
        #             print np.array(x_train_tf.todense()[i])[0].tolist()[j]
        #             for key in countVectorizer.vocabulary_:
        #                 if countVectorizer.vocabulary_[key] == j:
        #                     print key
        #             print
        #     print "--------------------"
        clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.0005)
        clf.fit(x_train_counts)
        x_train_counts = countVectorizer.transform(["what is the body of wines made in australia"])
        # x_train_tf = tfTransformer.transform(x_train_counts)
        print clf.predict(x_train_counts)
        vec_clf = Pipeline([('vectorizer', countVectorizer), ('clf', clf)])
        accuracy = self.accuracyCheck(classifier)
        filename = classifier + 'IntentClassifier.sav'
        joblib.dump(vec_clf, "ModelData/" + filename)
        print accuracy

        # trainSet = self.createTrainingSet()
        # # print trainSet
        # xTrain = list(trainSet[:, 0])
        # yTrain = list(trainSet[:, 1])
        # countVectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
        # xTrainCounts = countVectorizer.fit_transform(xTrain)
        # tfTransformer = TfidfTransformer()
        # xTrainTf = tfTransformer.fit_transform(xTrainCounts)
        # clf = svm.SVC(kernel='rbf', max_iter=-1, gamma=0.1)
        # x_train, x_test, y_train, y_test = train_test_split(xTrainTf, yTrain, test_size=0.3)
        # clf.fit(x_train, y_train)
        # predictions = clf.predict(x_test)
        # print accuracy_score(y_test, predictions)
        # vec_clf = Pipeline([('vectorizer', countVectorizer), ('tfVectorizer', tfTransformer), ('clf', clf)])
        # filename = 'intentClassifier.sav'
        # joblib.dump(vec_clf, "ModelData/" + filename)
        # print "Intent classifier successfully trained"


    def intentIdentifier(self, input):

        # processedSent = self.inputProcessing(input, False)
        # result = self.clf.predict([processedSent])
        # if int(result[0]) < 0:
        #     return ""
        # else:
        #     print self.intents["intents"][int(result[0])]["label"]
        #     return self.intents["intents"][int(result[0])]["label"]
        processedSent = self.inputProcessing(input, False)
        for intent in self.intents['intents']:
            result = self.classifiers[intent['label']].predict([processedSent])
            if result.astype(np.int64)[0] == -1:
                print intent['label']
                return intent['label']
        return ""


    def restoreClassifiers(self):
        classifiers = {}
        for intent in self.intents["intents"]:
            filename = intent["label"] + 'IntentClassifier.sav'
            clf = joblib.load("ModelData/" + filename)
            classifiers[intent["label"]] = clf
        return classifiers

    def accuracyCheck(self, classifier):
        testSet = self.createTestSet(classifier)
        predictions = self.classifiers[classifier].predict(list(testSet[:, 0]))
        score = 0
        yTest = testSet[:, 1].astype(np.int64)
        predictions = predictions.astype(np.int64)
        for i in range(0, len(yTest)):
            if yTest[i] == predictions[i]:
                score += 1
        accuracy = score/float(predictions.size)
        print accuracy
        return accuracy


intentClassifier = IntentClassifier()
intentClassifier.getDomainWords()
intentClassifier.createVocabulary()
# for intent in ["Color", "Sugar", "Flavor", "Body", "Grape", "Region", "Maker", "Wine"]:
intentClassifier.trainer("aboutColor")
# intentClassifier.intentIdentifier("what is the body of wines made in australia")
# print intentClassifier.vocabulary
