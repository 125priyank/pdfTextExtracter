import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from util import *

script_dir = os.path.dirname(__file__)

tmp = open(os.path.join(script_dir, 'tmp/matra.txt'), 'w', encoding='utf-8')
tmp.write(str(allMatra))
tmp.close()

class Pages:
    def __init__(self, pages):
        self.pages = pages
        self.paras = [[] for i in range(len(pages))]
        self.preprocess()
        self.prnt()

    def preprocess(self):
        for i in range(len(self.pages)):
            self.pages[i] = list(dict(sorted(self.pages[i].items(), reverse=True)).values())
            self.pages[i] = bottomMatraCorrector(self.pages[i])
            # sort chars wrt x-axis
            self.pages[i] = sortWrtXAxis(self.pages[i])

            self.paras[i] = rtPara(self.pages[i])

            mp = {'ष': 'र्', 'र्': 'ष'}
            self.paras[i] = replace(self.paras[i], mp)

            # Correct Matra
            self.paras[i] = matraCorrector(self.paras[i])

            self.paras[i] = txtCorrector(self.paras[i])

    def prnt(self):
        wrt = True
        prt = False
        if wrt:
            f = open(os.path.join(script_dir, 'tmp/gandhi.txt'), 'w', encoding='utf-8')
        s = ''
        for para in self.paras:
            for char in para:
                if wrt:
                    f.write(char['text'])
                    if char['text'] != '\n':
                        s += str(char)
                    else:
                        s += '\n'
                if prt:
                    print(char['text'], end='')

            f.write('\n\n\n\n')
        f.write(s)
        f.close()

uri = 'data/Munshi Premchand - गोदान Godan-Maple Press (2014).pdf'
uri = "data/gandhi-autobiography-hindi.pdf"

def fn():
    pages = []
    for page_layout in extract_pages(uri, page_numbers=[0,1,2,3,4,5]):
        ydict = {}
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            c = character.get_text()
                            x1, y1, x2, y2 = character.bbox
                            #if c in bottomMatra:
                                #print(character.bbox, c, x2-x1, y2-y1)
                            if y1 not in ydict:
                                ydict[y1] = []
                            ydict[y1].append({'bbox': character.bbox, 'text': c})
        pages.append(ydict)
    return Pages(pages)


pagesObj = fn()