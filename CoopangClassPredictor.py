from konlpy.tag import Komoran
from sklearn.naive_bayes import MultinomialNB
import pickle
import numpy as np

MODEL_FILE_NAME = './model/coopang_earphone_naive_bayes.model'
FEATURE_FILE_NAME = './model/coopang_earphone_naive_bayes.feature'

#unigram (1, 1), uni and bigram (1, 2), bigram(2,2)
NGRAM = (2, 2)

#CountVectorizer ngrams 함수만 가져옴.
def _word_ngrams(ngram_range, tokens, stop_words=None):
    """Turn tokens into a sequence of n-grams after stop words filtering"""
    # handle stop words
    if stop_words is not None:
        tokens = [w for w in tokens if w not in stop_words]

    # handle token n-grams
    min_n, max_n = ngram_range
    if max_n != 1:
        original_tokens = tokens
        if min_n == 1:
            # no need to do any slicing for unigrams
            # just iterate through the original tokens
            tokens = list(original_tokens)
            min_n += 1
        else:
            tokens = []

        n_original_tokens = len(original_tokens)

        # bind method outside of loop to reduce overhead
        tokens_append = tokens.append
        space_join = " ".join

        for n in range(min_n,
                       min(max_n + 1, n_original_tokens + 1)):
            for i in range(n_original_tokens - n + 1):
                tokens_append(space_join(original_tokens[i: i + n]))

    return tokens

#일반명사, 고유명사, 동사, 형용사, 보조용언, 긍정지정사, 부정지정사, 일반부사, 접속부사
SELECT_MORPH = {'NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MAG', 'MAJ'}

with open(FEATURE_FILE_NAME, 'rb') as featureFile:
    features = pickle.load(featureFile)

with open(MODEL_FILE_NAME, 'rb') as modelFile:
    classifier = pickle.load(modelFile)

#형태소분석기
komoran = Komoran()

while True:
    sentence = input("문장을 입력하세요(종료=exit): ")

    if sentence == 'exit':
        break

    analyzed = komoran.pos(sentence)
    selected = []

    for word, morph in analyzed:
        if morph in SELECT_MORPH:
            selected.append(word + '/' + morph)

    #document term array
    sentFeatures = np.zeros(shape=(1, len(features)))

    selected = _word_ngrams((1, 2), selected)

    for token in selected:
        featIdx = features.index(token) if token in features else -1

        if featIdx != -1:
            sentFeatures[0][featIdx] += 1

    print(sentFeatures[0])
    print(classifier.predict(sentFeatures))
