import nltk, re, pprint
from nltk.corpus import conll2000

# input = raw_input("Enter the question: ")
# sentences = nltk.sent_tokenize(input)
# print sentences
# sentences = [nltk.word_tokenize(sent) for sent in sentences]
# print sentences
# sentences = [nltk.pos_tag(sent) for sent in sentences]
# print sentences
# grammar = "NP: {<DT>?<JJ>*<NNS|NN>}"
# cp = nltk.RegexpParser(grammar)
# for sent in sentences:
#     result = cp.parse(sent)
#     print result

class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        # for i in train_sents:
        #     print nltk.chunk.tree2conlltags(i)
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

test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
print train_sents
unigram_chunker = UnigramChunker(train_sents)
# sentences = nltk.word_tokenize("How are you doing my baby")
# sentences = nltk.pos_tag(sentences)
# print unigram_chunker.parse(sentences)
print(unigram_chunker.evaluate(test_sents))
