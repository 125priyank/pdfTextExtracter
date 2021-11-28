from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from functools import cmp_to_key

allMatra = {'ं', 'र्', 'ँ', 'ं', 'ः', 'ऺ', 'ऻ', '़', 'ऽ', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॅ', 'ॆ', 'े', 'ै', 'ॉ', 'ॊ', 'ो', 'ौ', '्', 'ॎ', 'ॏ', 'ॐ', '॑', '॒', '॓', '॔', 'ॕ', 'ॖ', 'ॗ', 'ॢ', 'ॣ', 'ঁ'}
bottomMatra = {'्', 'ू', 'ु', 'ृ', 'ॄ'}
upMatra = {'ॅ', 'ॆ', 'े', 'ै', 'ऺ'}
tmp = open('G:\coding\o2.txt', 'w', encoding='utf-8')
tmp.write(str(allMatra))
tmp.close()

class Pages:
    def __init__(self, pages):
        self.pages = pages

    def preprocess(self):
        for i in range(len(self.pages)):
            self.pages[i] = list(dict(sorted(ydict.items(), reverse=True)).values())
a = extract_pages("C:/Users/Terminator/Downloads/gandhi-autobiography-hindi.pdf", page_numbers=[0,1])
print(type(a))
def fn():
    pages = []
    for page_layout in extract_pages("C:/Users/Terminator/Downloads/gandhi-autobiography-hindi.pdf", page_numbers=[0,1]):
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
    return pagesObj = Pages(pages)



ydict = fn()
ydict = list(dict(sorted(ydict.items(), reverse=True)).values())

def isAllMatra(string):
    if string == 'र्':
        return True
    for char in string:
        if char not in allMatra:
            return False
    return True
'''
Returns corrected bottom matra dict 
परी कथा शलख डालाँ और शफर वह पस्तक के रूप में छपे । मेंरे पास इकट ठा इतना समय 
्
ूूु
'''
i = 0
prevBottomMatra = -1
while i<len(ydict):
    isBottomMatra = True
    for j in ydict[i]:
        if j['text'] != ' ' and isAllMatra(j['text'])==False:
            isBottomMatra = False
            break
    if isBottomMatra:
        tmp = []
        for j in ydict[i]:
            if j['text'] != ' ':
                tmp.append(j)
        ydict[prevBottomMatra] += tmp
        ydict[i] = []
    else:
        prevBottomMatra = i
    i+=1

# Sort all chars wrt x-axis
def sortWrtXAxis(ydict):
    def sort_cmp(a, b):
        if a['bbox'][0] < b['bbox'][0]:
            return -1
        return 1
    
    for i in range(len(ydict)):
        if len(ydict[i])==0:
            continue
        ydict[i] = sorted(ydict[i], key=cmp_to_key(sort_cmp))
    return ydict


def rtPara(ydict):
    para = []
    for line in ydict:
        if len(line) == 0:
            continue
        for char in line:
            para.append(char)
        para.append({'bbox': (0, 0, 0, 0), 'text': '\n'})
    return para

# Return bbox obj with Corrected matra अधरूा अधूरा
def matraCorrector(para):
    for i in range(1, len(para)):
        if isAllMatra(para[i]['text']) and (para[i]['bbox'][0] - para[i-1]['bbox'][0] <= 3):
            para[i], para[i-1] = para[i-1], para[i]
    
    return para

def replace(para, mp):
    for i in range(len(para)):
        if para[i]['text'] in mp:
            para[i]['text'] = mp[para[i]['text']]

    return para
def txtCorrector(para):
    sh = 'श'
    harsikar = 'ि'
    for i in range(len(para)):
        if para[i]['text'] == sh:
            para[i]['text'] = harsikar
        elif para[i]['text'] == harsikar:
            para[i]['text'] = sh
    i=0
    while i<len(para)-1:
        if para[i]['text'] == harsikar:
            para[i]['text'], para[i+1]['text'] = para[i+1]['text'], para[i]['text']
            i+=2
        else:
            i+=1

    for i in range(len(para)-2):
        if para[i]['text']=='ह' and para[i+1]['text'] == 'ाँ':
            para[i+1]['text'] = 'ूँ'
            
    for i in range(len(para)):
        if para[i]['text'] == 'ाँ':
            para[i]['text'] = 'ँ'
            
    for i in range(len(para)-1):
        if para[i]['text'] == 'ँ' and isAllMatra(para[i+1]['text']) and len(para[i+1]['text']) == 1:
            if ord(para[i]['text']) < ord(para[i+1]['text']):
                para[i]['text'], para[i+1]['text'] = para[i+1]['text'], para[i]['text']
    
    i=1
    while i<len(para):
        if para[i]['text'] == 'र्':
            para[i]['text'], para[i-1]['text'] = para[i-1]['text'], para[i]['text']
        i+=1

    return para

# sort chars wrt x-axis
ydict = sortWrtXAxis(ydict)

para = rtPara(ydict)

mp = {'ष': 'र्', 'र्': 'ष'}
para = replace(para, mp)

# Correct Matra
para = matraCorrector(para)

para = txtCorrector(para)


wrt = True
prt = False
if wrt:
    f = open('G:\coding\o1.txt', 'w', encoding='utf-8')
s = ''
for char in para:
    if char['text']=='dnp':
        continue
    if wrt:
        f.write(char['text'])
        if char['text'] != '\n':
            s += str(char)
        else:
            s += '\n'
    if prt:
        print(char['text'], end='')

f.write('\n\n\n')
f.write(s)
f.close()