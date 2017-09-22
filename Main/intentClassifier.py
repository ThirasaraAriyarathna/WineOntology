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
        filename = 'intentClassifier.sav'
        self.clf = joblib.load("ModelData/" + filename)


    def getDomainWords(self):
        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.domainWords[subject[0]] = results

    def createVocabulary(self):
        for intent in self.intents["intents"]:
            self.vocabulary[intent["label"]] = []
            for subject in self.subjects:
                keywords = self.domainWords[subject[0]]
                for feature in intent["features"]:
                    if "<" and ">" in feature:
                        for keyword in keywords:
                            self.vocabulary[intent["label"]].append(re.sub('<' + subject[0] + '>', keyword.lower(), feature))
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
            if len(stemmedWords) < 10:
                stemmedSent = ' '.join(stemmedWords)
            else:
                stemmedSent = ' '.join(stemmedWords[:10])
        return stemmedSent


    def createTrainingSet(self):
        trainSet = []
        index = 0
        for intent in self.intents["intents"]:
            for sent in self.vocabulary[intent["label"]]:
                processedInput = self.inputProcessing(sent, True)
                trainSet.append([processedInput, index])
            index +=1
        trainSet = np.array(trainSet)
        return trainSet

    def trainer(self):
        trainSet = self.createTrainingSet()
        # print trainSet
        xTrain = list(trainSet[:, 0])
        yTrain = list(trainSet[:, 1])
        countVectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
        xTrainCounts = countVectorizer.fit_transform(xTrain)
        tfTransformer = TfidfTransformer()
        xTrainTf = tfTransformer.fit_transform(xTrainCounts)
        clf = svm.SVC(kernel='rbf', max_iter=-1, gamma=0.1)
        x_train, x_test, y_train, y_test = train_test_split(xTrainTf, yTrain, test_size=0.3)
        clf.fit(x_train, y_train)
        predictions = clf.predict(x_test)
        print accuracy_score(y_test, predictions)
        vec_clf = Pipeline([('vectorizer', countVectorizer), ('tfVectorizer', tfTransformer), ('clf', clf)])
        filename = 'intentClassifier.sav'
        joblib.dump(vec_clf, "ModelData/" + filename)
        print "Intent classifier successfully trained"

    def intentIdentifier(self, input):

        processedSent = self.inputProcessing(input, False)
        result = self.clf.predict([processedSent])
        if int(result[0]) < 0:
            return ""
        else:
            print self.intents["intents"][int(result[0])]["label"]
            return self.intents["intents"][int(result[0])]["label"]


# intentClassifier = IntentClassifier()
# intentClassifier.getDomainWords()
# intentClassifier.createVocabulary()
# intentClassifier.trainer()
# intentClassifier.intentIdentifier("In which wineries")
# print intentClassifier.vocabulary