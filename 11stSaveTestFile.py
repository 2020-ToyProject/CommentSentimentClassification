import os
import json
import pickle

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import accuracy_score
OUTPUT_FILE_NAME = "./model/11stBestModel.model"
TARGET_NAMES = ['긍정', '부정', '중립']
dirname2 = ('./data/강아지간식_분석')
dirname = ('./data/물티슈_분석')
sentenceFileList = os.listdir(dirname)
sentenceArr = []
labelArr = []

for sentenceFile in sentenceFileList:
    if (sentenceFile.endswith('txt')):
        # 문장 가져오기
        open_file = open(dirname + '/' + sentenceFile, 'r', encoding="utf-8")
        lines = open_file.readlines()
        open_file.close()
        for line in lines:
            try:
                dict = json.loads(line.rstrip())
                sentenceArr.append(' '.join(dict['custom_result']))
                if dict['rating']>3:
                    labelArr.append(TARGET_NAMES[0])
                elif dict['rating']<3:
                    labelArr.append(TARGET_NAMES[1])
                else:
                    labelArr.append(TARGET_NAMES[2])
            except Exception as e:
                print(e)

# 벡터 데이터 생성
vect = CountVectorizer(min_df=2, max_features=50000, ngram_range=(1, 3), tokenizer=lambda x: x.split(' '))
pipeline = Pipeline([
    ('vect', vect),
])
# 학습 데이터, 테스트 데이터로 나누기 전에 fit과 transform 으로 변환. fit_transform() 도 무방.
train_data_features = pipeline.fit_transform(sentenceArr)

# scale된 data로 학습셋, 테스트셋 분리
trainData, testData, trainLabel, testLabel = train_test_split(train_data_features, labelArr, test_size=0.3)

# 모델 선언
# svm 은 속성간의 의존성은 고려하지 않는다. 선형 분류 뿐 아니라 커널을 활용하여 다차원으로의 매핑도 가능하다
# 커널 종류로는 선형, 다항, 가우시안, 가우시안RBF, 라플라스RBF, 역탄젠트, 시그모이드, 제1종베셀함수 등등
clf = svm.SVC(kernel='linear')
clf_10 = svm.SVC(kernel='linear', C=10)
clf_rbf = svm.SVC(C=10.0, kernel='rbf', gamma=0.1)

# 교차검증 - 분산이 작으면 Overfitting 이 적다. 즉 예측율이 높음.
#avrScore = cross_val_score(clf, trainData, trainLabel, cv=6, scoring='accuracy')
#print('clf K-Fold 평균: {0:.4f}, 분산: {0:.4f}, 최소: {0:.4f}, 최대: {0:.4f}'.format(avrScore.mean(), avrScore.std(), avrScore.min(), avrScore.max()))
#avrScore = cross_val_score(clf_10, trainData, trainLabel, cv=6, scoring='accuracy')
#print('clf_1 K-Fold 평균: {0:.4f}, 분산: {0:.4f}, 최소: {0:.4f}, 최대: {0:.4f}'.format(avrScore.mean(), avrScore.std(), avrScore.min(), avrScore.max()))
#avrScore = cross_val_score(clf_rbf, trainData, trainLabel, cv=6, scoring='accuracy')
#print('clf_rbf K-Fold 평균: {0:.4f}, 분산: {0:.4f}, 최소: {0:.4f}, 최대: {0:.4f}'.format(avrScore.mean(), avrScore.std(), avrScore.min(), avrScore.max()))

# default svm 정확도 측정
#clf.fit(trainData, trainLabel)
#result = clf.predict(testData)
#print(metrics.classification_report(testLabel, result))

# svm rbf 정확도 측정
#clf_rbf.fit(trainData, trainLabel)
#result_rbf = clf_rbf.predict(testData)
#print(metrics.classification_report(testLabel, result_rbf))
#print('clf_rbf 예측 정확도: {0:.4f}'.format(accuracy_score(testLabel, result_rbf)))

# c와 gamma는 클수록 정확하고 작을수록 과대적합 방지 gamma는 결정경계의 곡률을 조정하며 rbf와 poly, sigmoid에서만 적용된다.
param_grid = [
    {'kernel': ['rbf'], 'gamma': [0.1, 0.5, 10, 1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
    {'kernel': ['poly'], 'gamma': [0.1, 0.5, 10, 1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
    {'kernel': ['linear'], 'C': [0.1, 1, 10, 100, 1000]}
]
clf_grid = GridSearchCV(svm.SVC(), param_grid, verbose=1)
clf_grid.fit(trainData, trainLabel)
result_grid = clf_grid.predict(testData)
print("Best Parameters:\n", clf_grid.best_params_)
print("Best Estimators:\n", clf_grid.best_estimator_)
print(metrics.classification_report(testLabel, result_grid))

#학습된 모델 객체 직렬화 파일 저장
with open(OUTPUT_FILE_NAME, 'w') as output:
    pickle.dump(clf_grid.best_estimator_, output)