import json
from konlpy.tag import *
import time

INPUT_FILE_NAME = './data/coopang_earphone_comments.txt'
OUTPUT_FILE_NAME = './data/analyzed_coopang_earphone_comments_all.txt'

#일반명사, 고유명사, 동사, 형용사, 보조용언, 긍정지정사, 부정지정사, 일반부사, 접속부사
SELECT_MORPH = {'NNG', 'NNP', 'VV', 'VA', 'VX', 'VCP', 'VCN', 'MAG', 'MAJ'}

#pip install JPype1==0.7.0
komoran = Komoran()
# hannanum = Hannanum()
# kkma = Kkma()
#okt = Okt()

outputFile = open(OUTPUT_FILE_NAME, mode='w', encoding='utf-8')
inputFile = open(INPUT_FILE_NAME, mode='rt', encoding='utf-8')

#print(komoran.tagset)

start = time.time()
countContentNull = 0
countContentExist = 0

for data in inputFile.readlines():
    #if countContentExist == 1000:
    #    break

    try:
        dict = json.loads(data, encoding='utf-8')
    except Exception:
        continue

    #데이터 처리양이 많아지면 string concat 효율성 고려하기
    text = ''

    if 'comment_title' in dict:
        text += dict['comment_title'] + "\n"
    if 'comment_content' in dict:
        text += dict['comment_content']

    if text == '':
        countContentNull += 1
        continue
    else:
        countContentExist += 1

    #사용할 형태소 선택
    analyzed = komoran.pos(text)
    selected = []
    for word, morph in analyzed:
        if morph in SELECT_MORPH:
            selected.append(word+'/'+morph)

    #추출된 값이 없으면 데이터 제거
    if len(selected) == 0:
        continue
        
    #감정 태깅
    emotion = ''
    if dict['rating'] == '1' or dict['rating'] == '2':
        emotion = '부정'
    elif dict['rating'] == '3':
        emotion = '중립'
    else:
        emotion = '긍정'

    outputFile.write(emotion + '\t')
    outputFile.write(','.join(selected))
    outputFile.write('\n')

    #komoran.pos(text)
    #hannanum.pos(text)
    #kkma.pos(text)
    #okt.pos(text)

print("time :", time.time() - start)

outputFile.close()
inputFile.close()