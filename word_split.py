import re
import os


class WordSplit(object):
    """
    split words from local path.
    """

    def __init__(self, path, min_length=3):
        super(WordSplit, self).__init__()
        self.path = path
        self.min_length = min_length

    def run(self):
        with open(self.path, 'r', encoding='gb18030') as f:
            buffer = [line for line in f.readlines()]
            if len(buffer):
                return self.extract(''.join(buffer))

    def extract(self, text):
        r = re.findall('[a-z]{1,}\s', text)
        words = [word.replace(' ', '').replace('\n', '').replace('\t', '') for word in r]
        words = list(filter(lambda x: len(x) > 1, words))
        words.sort()
        return words


if __name__ == '__main__':
    ws = WordSplit(f'{os.getcwd()}/paper/high/2018年高考英语真题语法填空合集.txt')
    r = ws.run()
    print(r)
