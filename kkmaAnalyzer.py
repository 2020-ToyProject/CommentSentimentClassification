import os
import json
import re
from konlpy.tag import Kkma
kkma = Kkma()

def clean_consonant_vowels(text):
  pattern='[ㄱ-ㅎㅏ-ㅣ]+'
  repl=''
  cleaned_text = re.sub(pattern, repl, text)
  return cleaned_text

analyzedDirectoryName = ('./data/강아지간식_분석/')
# 파일 loading

# 문장 가져오기
open_file = open('./data/allStar_강아지간식.txt', 'r', encoding="utf-8")
lines = open_file.readlines()
open_file.close()

new_file = open(analyzedDirectoryName+'allStar_강아지간식_분석.txt', 'w', encoding="utf-8")
for line in lines:
    try:
        dict = json.loads(line.rstrip())
        # 띄어쓰기 형보정

        # 띄어쓰기 진행하고도 100자가 넘는데 띄어쓰기가 10개가 안넘어가면 pass

        # 자음/모음 모임 정제
        cleandContent = clean_consonant_vowels(dict['comment_content'])
        # cleandContent = dict['comment_content']
        # 형분석
        if len(cleandContent) > 0:
            posTaggingResult = kkma.pos(cleandContent)
            #morphResult = kkma.morphs(cleandContent)
            customResult = []
            morphResult = []
            for pos in posTaggingResult:
                if pos[1] == "NNP" or pos[1] == "NNG" or pos[1] == "VV" or pos[1] == "VA" or pos[1] == "VCP" or pos[1] == "VCN":
                    customResult.append(pos[0]+"/"+pos[1])
                morphResult.append(pos[0]+"/"+pos[1])
            dict['morph_result'] = morphResult
            dict['custom_result'] = customResult
            json.dump(dict, new_file, ensure_ascii=False)
            new_file.write('\n')
    except Exception as e:
        print(e)
new_file.close()