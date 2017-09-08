from queryGenerator import QueryGenerator
import nltk


class EntityExtractor:

    keywords = {}
    subjects = [("sugar", "WineSugar"), ("flavor", "WineFlavor"), ("maker", "Winery"), ("region", "Region"),
                ("color", "WineColor"), ("grape", "WineGrape"), ("body", "WineBody"), ("wine", "hasMaker")]
    queryGenerator = QueryGenerator()

    def __init__(self):
        self.getKeywords()


    def entityDetector(self, conditions, inputString):

        inputWords = nltk.word_tokenize(inputString)
        for key in conditions:
            if conditions[key][0] ==1 and len(conditions[key][1]) == 0:
                isPresent = False
                for word in inputWords:
                    for keyword in self.keywords[key]:
                        if word.lower() == keyword.lower():
                            conditions[key][1] = keyword
                            isPresent = True
                            break
                    if isPresent:
                        break
                if not(isPresent):
                    return False, key, self.keywords[key], conditions
        return True, conditions

    def getKeywords(self):

        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.keywords[subject[0]] = results
        print self.keywords
