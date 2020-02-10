import os
import json
from konlpy.tag import Kkma
kkma = Kkma()

dirname = ('./data')
# 파일 loading
sentenceFileList = os.listdir(dirname)
for sentenceFile in sentenceFileList:
    print(sentenceFile)
    # 문장 가져오기
    open_file = open(dirname+'/'+sentenceFile, 'r', encoding="utf-8")
    sentence = sentenceFile.title()
    lines = open_file.readlines()
    open_file.close()

    new_file = open(dirname+'/analyze/'+sentenceFile, 'w', encoding="utf-8")
    for line in lines:
        dict = json.loads(line.rstrip())

        # 형분석
        posTaggingResult = kkma.pos(dict['comment_content'])
        morphResult = kkma.morphs(dict['comment_content'])
        customResult = []
        for pos in posTaggingResult:
            if pos[1] == "NNP" or pos[1] == "NNG" or pos[1] == "VV":
                customResult.append(pos[0])

        dict['morphResult'] = morphResult
        dict['customResult'] = customResult
        json.dump(dict, new_file, ensure_ascii=False)
        new_file.write('\n')
    new_file.close()
# 띄어쓰기 보정

# 파일 저장