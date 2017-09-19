from queryGenerator import QueryGenerator
import re
from nltk.stem.porter import PorterStemmer

class EntityExtractor:

    keywords = {}
    subjects = [("sugar", "WineSugar"), ("flavor", "WineFlavor"), ("maker", "Winery"), ("region", "Region"),
                ("color", "WineColor"), ("grape", "WineGrape"), ("body", "WineBody"), ("wine", "hasMaker")]
    queryGenerator = QueryGenerator()

    def __init__(self):
        self.getKeywords()


    def entityDetector(self, conditions, entities):

        for key in conditions:
            if conditions[key][0] == 1 and entities[key][0] == 0:
                entities[key][0] = 1
                for word in conditions[key][1].split():
                    isPresent = False
                    for keyword in self.keywords[key]:
                        if word.lower() in self.keywords[key][keyword]:
                            entities[key].append(keyword)
                            isPresent = True
                            break
                    if isPresent:
                        break
                if not(isPresent):
                    entities[key][0] = 0
                    return False, key, entities
        # print entities
        return True, entities

    def getKeywords(self):

        stemmer = PorterStemmer()
        for subject in self.subjects:
            queryElements = self.queryGenerator.assembler("info",  subject)
            results = self.queryGenerator.queryExecuter(queryElements[0], queryElements[1])
            self.keywords[subject[0]] = results
        for key in self.keywords:
            keys = {}
            for dword in self.keywords[key]:
                arr = [dword]
                expanded_word = re.findall('[A-Z][^A-Z]*', dword)
                for word in expanded_word:
                    if word in ['Winery', 'Wine', 'Grape', 'Region']:
                        expanded_word.remove(word)
                arr.append(''.join(expanded_word).lower())
                arr.append(stemmer.stem(''.join(expanded_word)))
                arr.append(' '.join(expanded_word).lower())
                if dword == 'Dry':
                    arr.extend(['low', 'less'])
                elif dword == 'OffDry':
                    arr.extend(['moderate', 'medium', 'average'])
                elif dword == 'Sweet':
                    arr.extend(['high', 'most', 'more'])
                keys[dword] = arr
            self.keywords[key] = keys
