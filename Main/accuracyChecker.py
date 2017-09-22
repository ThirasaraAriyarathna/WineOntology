import json
from botMain import WineChatbot
from botMain import UnigramChunker
class AccuracyChecker:

    def __init__(self):
        self.conditions = ["color", "wine", "sugar", "flavor", "body", "grape", "maker", "region"]
        with open('test.json') as json_data:
            self.tests = json.load(json_data)
        self.testSamples = []
        for test in self.tests['tests']:
            self.testSamples.append(test['test'])

    def accuracyCheck(self):
        chatbot = WineChatbot()
        results = chatbot.main(True, self.testSamples)
        intent_accuracy = 0
        condition_accuracy = 0
        overall = 0
        accuracies = {}
        for condition in self.conditions:
            accuracies[condition] = 0
        index = 0
        for test in self.tests['tests']:
            intent_false = False
            condition_false = False
            if test['response']['intent'] == results[index][0]:
                intent_accuracy += 1
            else:
                intent_false = True
            for condition in self.conditions:
                if test['response'][condition] == results[index][1][condition][0]:
                    accuracies[condition] += 1
                else:
                    condition_false = True
            if not condition_false:
                condition_accuracy += 1
                if not intent_false:
                    overall += 1
            index += 1
        print "Intent Accuracy: " + str(intent_accuracy/float(len(self.testSamples)))
        print "Condition Accuracy: " + str(condition_accuracy/float(len(self.testSamples)))
        print "Overall Accuracy: " + str(overall/float(len(self.testSamples)))
        for condition in self.conditions:
            print condition + " Accuracy:" + str(accuracies[condition]/float(len(self.testSamples)))


accuracyChecker = AccuracyChecker()
accuracyChecker.accuracyCheck()