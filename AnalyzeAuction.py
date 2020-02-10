from konlpy.tag import Hannanum
import json

hannanum = Hannanum()

hannanum.analyze  # 구(Phrase) 분석
hannanum.morphs  # 형태소 분석
hannanum.nouns  # 명사 분석
hannanum.pos  # 형태소 분석 태깅

i = 0;
with open('./data/auctionComment_영양제.json', 'rt', encoding='UTF8') as json_file:
    for line in json_file:
        try:
            y = json.loads(line)
            # json_data = json.load(line)
            # print(json_data["product_title"])

            y["analyze"] = hannanum.analyze(y["comment_content"])
            y["morphs"] = hannanum.morphs(y["comment_content"])
            y["pos"] = hannanum.pos(y["comment_content"])
            y["nouns"] = hannanum.nouns(y["comment_content"])

            print(y);
            with open("data/analyzed_영양제.json", "a", encoding="utf-8") as fp:
                json.dump(y, fp, ensure_ascii=False)
                fp.write("\n")

            i = i + 1
            if i == 2000:
                break
        except Exception as e:
            print(e)
