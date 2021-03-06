from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics
import json
import pickle
import time

SENTENCE_FILE_NAME = './data/analyzed_coopang_earphone_normalized_comments.txt'
MODEL_FILE_NAME = './model/coopang_earphone_naive_bayes.model'
FEATURE_FILE_NAME = './model/coopang_earphone_naive_bayes.feature'

#unigram (1, 1), uni and bigram (1, 2), bigram(2,2)
NGRAM = (1, 2)
TARGET_NAMES = ['긍정', '부정', '중립']

inputFile = open(SENTENCE_FILE_NAME, mode='rt', encoding='utf-8')

start = time.time()

#정답 레이블
label = []
#feature에 해당하는 문장 리스트
sentences = []

#학습 가능한 데이터로 전처리
for data in inputFile.readlines():
    try:
        dict = json.loads(data, encoding='utf-8')
    except Exception:
        continue

    emotion = ''

    if int(dict['rating']) == 1 or int(dict['rating']) == 2:
        emotion = '부정'
    elif int(dict['rating']) == 3:
        emotion = '중립'
    else:
        emotion = '긍정'

    label.append(emotion)
    sentences.append(' '.join(dict['morph_result']))

#벡터 데이터 생성
#ngram 적용, tokenizing은 공백단위, 형태소태그는 그대로 사용하기 위해 lowercase 미적용
vectorizer = CountVectorizer(ngram_range=NGRAM, tokenizer=lambda x: x.split(' '),
                             min_df=5, max_features=50000, lowercase=False)
# vectorizer = TfidfVectorizer(ngram_range=NGRAM, tokenizer=lambda x: x.split(' '),
#                              lowercase=False, min_df=5, max_features=20000)

vectMatrix = vectorizer.fit_transform(sentences)

#학습셋, 테스트셋 분리
trainData, testData, trainLabel, testLabel = train_test_split(vectMatrix, label, test_size=0.3)

#학습셋으로 K fold validating
accuracys = cross_val_score(MultinomialNB(), trainData, trainLabel, cv=6, scoring='accuracy')
print("학습셋 K-Fold Validating 평균 정확도 : ", accuracys.mean())

#별도의 테스트셋으로 검증
classifier = MultinomialNB().fit(trainData, trainLabel)

testPredition = classifier.predict(testData)
print(metrics.classification_report(testLabel, testPredition, target_names=TARGET_NAMES))
print(metrics.confusion_matrix(testLabel, testPredition, labels=TARGET_NAMES))

#학습된 모델 객체 직렬화 파일 저장
with open(MODEL_FILE_NAME, 'wb') as output:
    pickle.dump(classifier, output)

#모델 feature 리스트 파일 저장
with open(FEATURE_FILE_NAME, 'wb') as output:
    pickle.dump(vectorizer.get_feature_names(), output)

inputFile.close()
