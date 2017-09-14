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

    def main(self):

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
                hasMeaning = False
                for key in conditions:
                    if conditions[key][0] == 1:
                        hasMeaning = True
                        break
                if hasMeaning:
                    entities = self.entityExtractor.entityDetector(conditions, req)
                    while not(entities[0]):
                        print("please specify the type of " + entities[1] + " you want")
                        print("Available " + entities[1] + "s are")
                        print(entities[2])
                        newEntity = raw_input("bot$ ")
                        req += newEntity
                        entities = self.entityExtractor.entityDetector(entities[3], req)
                    queryElements = self.queryGenerator.assembler(intent, entities[1])
                    results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
                    if len(results) == 0:
                        print("we couldn't find any matching results in the ontology. Any other questions about wines?")
                    else:
                        for result in results:
                            print result
                else:
                    print("Please specify what you want to know about wines")

            req = raw_input("bot$ ")

chatbot = WineChatbot()
chatbot.main()