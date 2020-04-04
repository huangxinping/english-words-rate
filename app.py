from word_split import WordSplit
from word_translate import WordTranslate
import os
import pymongo

client = pymongo.MongoClient(os.getenv('MONGO_HOST', '192.168.0.210'), os.getenv('MONGO_PORT', 27017))
db = client.english_words_rate


def scan_high_school():
    word_counter = {}
    base_path = f'{os.getcwd()}/paper/high'
    for path in os.listdir(base_path):
        if '.txt' in path:
            ws = WordSplit(f'{base_path}/{path}')
            for word in ws.run():
                if word not in word_counter:
                    word_counter[word] = 1
                else:
                    word_counter[word] += 1

    # use counter as sort function.
    word_counter = {k: v for k, v in sorted(word_counter.items(), key=lambda item: item[1], reverse=True)}
    # with open(f'{os.getcwd()}/words.csv', 'w+') as f:
    #     f.write('word,number\n')
    #     for k, v in word_counter.items():
    #         f.write(f'{k},{v}\n')
    for word in word_counter:
        print('*' * 20)
        cursor = db.high.find({'word': word})
        if cursor.count() > 0:
            print(f'过滤掉 {word}')
            continue
        print(f'正在处理 {word}')
        wt = WordTranslate(word)
        r = wt.run()
        if r:  # Maybe translate action is not successful.
            r = r.copy()
            r['word'] = word  # add it to dictionary.
            db.high.insert_one(r)


if __name__ == '__main__':
    try:
        scan_high_school()
    except Exception as e:
        print(e)
