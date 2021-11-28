from functools import cmp_to_key
allMatra = {'ं', 'ँ', 'ं', 'ः', 'ऺ', 'ऻ', '़', 'ऽ', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॅ', 'ॆ', 'े', 'ै', 'ॉ', 'ॊ', 'ो', 'ौ', '्', 'ॎ', 'ॏ', 'ॐ', '॑', '॒', '॓', '॔', 'ॕ', 'ॖ', 'ॗ', 'ॢ', 'ॣ', 'ঁ'}
bottomMatra = {'्', 'ू', 'ु', 'ृ', 'ॄ'}
upMatra = {'ॅ', 'ॆ', 'े', 'ै', 'ऺ'}
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
def bottomMatraCorrector(ydict):
    prevTxt = 0
    for i in range(1, len(ydict)):
        allspaceflg = True
        for char in ydict[i]:
            if char['text'] != ' ':
                allspaceflg = False
                break
        if len(ydict[i]) == 0 or allspaceflg:
            ydict[i]=[]
            continue
        
        if abs(ydict[prevTxt][0]['bbox'][1]-ydict[i][0]['bbox'][1]) <= 5:
            ydict[prevTxt] += ydict[i]
            ydict[i] = []
        else:
            prevTxt = i
    return ydict


    
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
    return ydict

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
            # BUG: आध्यात्िमक
            if i+2 < len(para) and len(para[i+1]['text']) == 2 and para[i+1]['text'][1]=='्':
                para[i]['text'], para[i+1]['text'] = para[i+1]['text'], para[i]['text']
                para[i+1]['text'], para[i+2]['text'] = para[i+2]['text'], para[i+1]['text']
                i+=3
            else:
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

    i=0
    while i<len(para):
        j = i
        tmp = []
        while i < len(para) and para[i]['text'] in allMatra:
            tmp.append(para[i]['text'])
            i+=1
        if i>j:
            tmp = sorted(tmp, reverse=True)
            while j<i:
                para[j]['text']=tmp.pop(0)
                j+=1
        else:
            i+=1
    
    i=1
    while i<len(para):
        if para[i]['text'] == 'र्':
            para[i]['text'], para[i-1]['text'] = para[i-1]['text'], para[i]['text']
        i+=1

    return para