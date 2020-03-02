import os
import json

dirname = ('./data/강아지간식/star5')
saveDirectoryName = ('./data/')
# 파일 loading
sentenceFileList = os.listdir(dirname)
new_file = open(saveDirectoryName + 'allStar_강아지간식.txt', 'a', encoding="utf-8")
for sentenceFile in sentenceFileList:
    print(sentenceFile)
    if sentenceFile.endswith('txt'):
        # 문장 가져오기
        open_file = open(dirname + '/' + sentenceFile, 'r', encoding="utf-8")
        lines = open_file.readlines()
        open_file.close()
        for line in lines:
            try:
                dict = json.loads(line.rstrip())
                json.dump(dict, new_file, ensure_ascii=False)
                new_file.write('\n')
            except Exception as e:
                print(e)
new_file.close()
