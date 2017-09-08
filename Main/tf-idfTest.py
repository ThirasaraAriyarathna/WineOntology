from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string

train_set = ("The sky is blue.", "The sun is bright.")
test_set = ("The sun in the sky is bright.", "We can see the shining sun, the bright sun.")

count_vectorizer = CountVectorizer()
print count_vectorizer

count_vectorizer.fit_transform(train_set)
print "Vocabulary:", count_vectorizer.vocabulary_
# Vocabulary: {'blue': 0, 'sun': 1, 'bright': 2, 'sky': 3}
smatrix = count_vectorizer.transform(test_set)
print smatrix
freq_term_matrix = count_vectorizer.transform(test_set)
print freq_term_matrix.todense()

sent = "what are the wines having"
mess = [char for char in sent if char not in string.punctuation]
nopunc = ''.join(mess)
cleanMess = [word for word in nopunc.split() if word not in ENGLISH_STOP_WORDS]
print cleanMess