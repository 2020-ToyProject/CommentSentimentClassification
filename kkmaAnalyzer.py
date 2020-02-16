import os
import json
from konlpy.tag import Kkma
kkma = Kkma()

dirname = ('./data')
# 파일 loading
sentenceFileList = os.listdir(dirname)
for sentenceFile in sentenceFileList:
    print(sentenceFile)
    if(sentenceFile.endswith('txt')):
        # 문장 가져오기
        open_file = open(dirname+'/'+sentenceFile, 'r', encoding="utf-8")
        sentence = sentenceFile.title()
        lines = open_file.readlines()
        open_file.close()

        new_file = open(dirname+'/analyze2/'+sentenceFile, 'w', encoding="utf-8")
        for line in lines:
            try:
                dict = json.loads(line.rstrip())
                # 띄어쓰기 형보정

                # 띄어쓰기 진행하고도 100자가 넘는데 띄어쓰기가 10개가 안넘어가면 pass

                # 형분석
                posTaggingResult = kkma.pos(dict['comment_content'])
                morphResult = kkma.morphs(dict['comment_content'])
                customResult = []
                for pos in posTaggingResult:
                    if pos[1] == "NNP" or pos[1] == "NNG" or pos[1] == "VV" or pos[1] == "VA" or pos[1] == "VCP" or pos[1] == "VCN":
                        customResult.append(pos[0])

                dict['morphResult'] = morphResult
                dict['customResult'] = customResult
                json.dump(dict, new_file, ensure_ascii=False)
                new_file.write('\n')
            except Exception as e:
                print(e)
        new_file.close()
# 띄어쓰기 보정

# 파일 저장