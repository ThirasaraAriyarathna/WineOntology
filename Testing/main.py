
from Main.queryGenerator import QueryGenerator
from languageProcessor import LanguageProcessor

'''
Possible questions

-what are the available <low> sugar wines?
-what are the matching wines for <food>?
-what are the wines produced from <winery>?
-what are the available <strong> flavor wines?
'''
class WineChatbot():
    keywords = {}
    subjects = [("sugar", "WineSugar"), ("flavor", "WineFlavor"), ("maker", "Winery"), ("region", "Region"), ("color", "WineColor"), ("grape", "WineGrape"), ("body", "WineBody"), ("wine", "hasMaker")]
    languageProcessor = LanguageProcessor()
    queryGenerator = QueryGenerator()

    def main(self):
        self.languageProcessor.createVocabulary(self.keywords)
        self.languageProcessor.trainer()
        req = raw_input("bot$ ")
        req.strip()
        while len(req) > 0:
            intent = self.languageProcessor.intentIdentifier(req)
            if len(intent) == 0:
                print "Try another way"
            else:
                # arr = [w.lower() for w in self.keywords[intent]]
                entities = self.languageProcessor.entityExtractor(req, intent, self.keywords)
                if len(entities) > 0:
                    results = self.queryGenerator.processor(intent, False, entities)
                    for key in results:
                        for i in results[key]:
                            print i
                else:
                    print "No any specific keywords found. Please make your question more specific"
            req = raw_input("bot$ ")

    # def getInfo(self):
    #
    #     for subject in self.subjects:
    #         results = self.queryGenerator.processor("info", True, [subject[1]])
    #         self.keywords[subject[0]] = results["keywords"]
    #     print self.keywords

    def getInfo(self):

        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.keywords[subject[0]] = results
        print self.keywords


chatbot = WineChatbot()
chatbot.getInfo()
# chatbot.main()
