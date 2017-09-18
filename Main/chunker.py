import nltk
import json
import re
import string
from queryGenerator import QueryGenerator
from nltk.stem.porter import PorterStemmer
import pickle

class Chuncker:

    with open('intents2.json') as json_data:
        intents = json.load(json_data)
    domainWords = {}
    vocabulary = {}
    subjects = [("sugar", "WineSugar"), ("flavor", "WineFlavor"), ("maker", "Winery"), ("region", "Region"),
                ("color", "WineColor"), ("grape", "WineGrape"), ("body", "WineBody"), ("wine", "hasMaker")]
    queryGenerator = QueryGenerator()


    def __init__(self):
        filename = "UnigramChunker.sav"
        self.unigram_chunker = pickle.load(open('ModelData/' + filename, 'rb'))
        # pass

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
                for keyword in keywords:
                    self.vocabulary[intent["label"]].append(re.sub('<' + intent["label"] + '>', keyword.lower(), feature))

    def inputCleaning(self, inputArray):
        outputArray = []
        for sent in inputArray:
            arr = [char for char in sent if char not in string.punctuation]
            noPunc = ''.join(arr)
            outputArray.append(noPunc)
        # tokanizedWords = nltk.word_tokenize(noPunc)
        # stemmedWords = [self.stemmer.stem(word.lower()) for word in tokanizedWords]
        # stemmedSent = ' '.join(stemmedWords)
        return outputArray

    def chunck(self, input):

        clean_sent = self.inputCleaning([input])
        sent = nltk.word_tokenize(clean_sent[0])
        tagged_sent = nltk.pos_tag(sent)
        chunked_sent = self.unigram_chunker.parse(tagged_sent)

        chunks = []
        tagged_chunks = []
        for subtree in chunked_sent.subtrees():
            if subtree.label() == 'NP':
                words = [w for w, t in subtree.leaves()]
                tags = [t for w, t in subtree.leaves()]
                if len(tags) >= 2:
                    if tags[0] == 'JJ' and tags[1] != 'VBZ':
                        for i in range(1, len(tags)):
                            if tags[i] == 'JJ':
                                chunks.append(words[i-1] + ' wine')
                            else:
                                chunks.append(words[i-1] + ' ' + PorterStemmer().stem(words[i]))
                    else:
                        chunks.append(' '.join(words))
                    tagged_chunks.append(subtree.leaves())
        print chunks
        return chunks, tagged_chunks

    def createTrainingSet(self):

        grammar = r"""
                          NP:
                            {<VBD|VBN>?<IN><JJ|NN|NNP|NNS><NN|NNP|NNS>?}
                            {<VBD|VBN><VBG><JJ|NN|NNP|NNS><NN|NNP|NNS>?}
                            {<JJ><NN><VBZ><JJ|NN|NNP|NNS><NN|NNP|NNS>?}
                            {<JJ>+<VBD|VBN|NN|NNS|NNP>}
                            {<NN><NN|VBD>}
                            {<NN|NNS|NNP>}
                          """
        cp = nltk.RegexpParser(grammar)
        train_sents = []

        for key in self.vocabulary:
            cleaned_sents = self.inputCleaning(self.vocabulary[key])
            tokenized_sents = [nltk.word_tokenize(sent) for sent in cleaned_sents]
            tagged_sents = [nltk.pos_tag(sent) for sent in tokenized_sents]
            arr = []
            for sent in tagged_sents:
                result = cp.parse(sent)
                arr.append(result)
            train_sents.extend(arr)
        return train_sents

    def trainTagger(self, train_sents):

        self.unigram_chunker = UnigramChunker(train_sents)
        filename = "UnigramChunker.sav"
        pickle.dump(self.unigram_chunker, open('ModelData/' + filename, 'wb'))


class UnigramChunker(nltk.ChunkParserI):

    def __init__(self, train_sents):
        for i in train_sents:
            print nltk.chunk.tree2conlltags(i)
        train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)

# test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
# train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
# print train_sents
# unigram_chunker = UnigramChunker(train_sents)
# print(unigram_chunker.evaluate(test_sents))


# chunker = Chuncker()
# chunker.chunck("what are the available red wines made in australia")
# chunker.getDomainWords()
# chunker.createVocabulary()
# train_sents = chunker.createTrainingSet()
# chunker.trainTagger(train_sents)
# sentences = nltk.word_tokenize("What are the red wines made in Australia")
# sentences = nltk.pos_tag(sentences)
# print unigram_chunker.parse(sentences)