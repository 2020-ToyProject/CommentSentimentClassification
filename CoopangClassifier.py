from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics
import pickle
import time

INPUT_FILE_NAME = './data/analyzed_coopang_earphone_comments_all.txt'
OUTPUT_FILE_NAME = './model/coopang_earphone_naive_bayes.model'
#unigram(1,1), bigram(1,2)
NGRAM = [1, 2]
TARGET_NAMES = ['긍정', '부정', '중립']

inputFile = open(INPUT_FILE_NAME, mode='rt', encoding='utf-8')

start = time.time()

#정답 레이블
label = []
#feature에 해당하는 문장 리스트
sentences = []

lineIdx = 0

#학습 가능한 데이터로 전처리
for data in inputFile.readlines():
    labelAndData = data.split("\t")

    label.append(labelAndData[0])
    sentences.append(labelAndData[1].replace(",", " "))

    lineIdx += 1

#print(label)
#print(sentences)

#CountVectorizer를 사용하되 메모리에 로드될 데이터가 너무 큰 경우에
#HashingVectorizer를 사용한다.
#벡터 데이터 생성
#ngram 적용, tokenizing은 공백단위
vectMatrix = CountVectorizer(ngram_range=(1, 2), tokenizer=lambda x: x.split(' '), min_df=5).fit_transform(sentences)
vector = vectMatrix.toarray()

#학습셋, 테스트셋 분리
trainData, testData, trainLabel, testLabel = train_test_split(vector, label, test_size=0.3)

#학습셋으로 K fold validating
accuracys = cross_val_score(MultinomialNB(), trainData, trainLabel, cv=6, scoring='accuracy')
print("학습셋 K-Fold Validating 평균 정확도 : ", accuracys.mean())

#별도의 테스트셋으로 검증
classifier = MultinomialNB().fit(trainData, trainLabel)

testPredition = classifier.predict(testData)
print(metrics.classification_report(testLabel, testPredition, target_names=TARGET_NAMES))

#학습된 모델 객체 직렬화 파일 저장
with open(OUTPUT_FILE_NAME, 'wb') as output:
    pickle.dump(classifier, output)

inputFile.close()
