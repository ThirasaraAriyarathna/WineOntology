from intentClassifier import IntentClassifier
from conditionClassifier import ConditionClassifier
from entityExtractor import EntityExtractor
from queryGenerator import QueryGenerator
from chunker import Chuncker
from chunker import UnigramChunker


class WineChatbot:

    def __init__(self):
        self.intentClassifier = IntentClassifier()
        self.conditionClassifier = ConditionClassifier()
        self.entityExtractor = EntityExtractor()
        self.queryGenerator = QueryGenerator()
        self.chunker = Chuncker()

    def main(self, test, test_inputs):

        if test:
            test_results = []
            test_index = 0
            req = test_inputs[test_index]
        else:
            req = raw_input("bot$ ")
        req.strip()
        while len(req) > 0:
            intent = self.intentClassifier.intentIdentifier(req)
            if len(intent) == 0:
                print "Didn't get it! Try another way"
            else:
                chunks = self.chunker.chunck(req)
                tagged_chunks = chunks[1]
                chunks = chunks[0]
                conditions = self.conditionClassifier.conditionIndentifier(intent, chunks)
                if not test:
                    hasMeaning = False
                    for key in conditions:
                        if conditions[key][0] == 1:
                            hasMeaning = True
                            break
                    if hasMeaning:
                        entity_arr = {}
                        for key in conditions:
                            entity_arr[key] = [0]
                        entities = self.entityExtractor.entityDetector(conditions, entity_arr)
                        while not(entities[0]):
                            print("please specify the " + entities[1] + " you want")
                            print("Available " + entities[1] + "s are")
                            print([keyword for keyword in self.entityExtractor.keywords[entities[1]]])
                            newEntity = raw_input("bot$ ")
                            conditions[entities[1]][1] = newEntity
                            entities = self.entityExtractor.entityDetector(conditions, entities[2])
                        queryElements = self.queryGenerator.assembler(intent, entities[1])
                        results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
                        if len(results) == 0:
                            print("we couldn't find any matching results in the ontology. Any other questions about wines?")
                        else:
                            for result in results:
                                print result
                    else:
                        print("Please specify what you want to know about wines")

            if test:
                test_results.append([intent, conditions])
                if len(test_inputs) == test_index + 1:
                    return test_results
                else:
                    test_index += 1
                    req = test_inputs[test_index]
            else:
                req = raw_input("bot$ ")

# chatbot = WineChatbot()
# chatbot.main(False, [])
