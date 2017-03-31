#encoding=utf-8
import jieba

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
import codecs
def doSeg(filename):
    f = open(filename, 'r+')
    file_list = f.read()
    f.close()
    seg_list = jieba.cut(file_list)

    tokens = []
    for seg in seg_list:
        if (seg.encode("utf-8") not in stopwords and seg != '' and seg != '\n' and seg != '\n\n'):
            tokens.append(seg)

    return tokens
allmap = {}
def loadWordNet():
    f = codecs.open('./cow-not-full.txt', 'rb', 'utf-8')
    known = set()
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        row = line.strip().split('\t')
        if len(row) == 3:
            (synset, lemma, status) = row
        elif len(row) == 2:
            (synset, lemma) = row
            status = 'Y'
        else:
            print 'bad formed line:', line.strip()
        if status in ['Y', 'O']:
            if not (synset.strip(), lemma.strip()) in known:
                #print synset.strip(), lemma.strip()
                known.add((synset.strip(), lemma.strip()))
                if allmap.get(lemma.strip()) != None:
                    allmap[lemma.strip()] = allmap[lemma.strip()].append(synset.strip())
                else:
                    allmap[lemma.strip()] = [synset.strip()]


    return known

def findWordNet(known, key):
    tokens = []
    #print key.encode('utf-8')
    value = allmap.get(key)
    if value is not None:
        for innervalue in value:
            tokens.append(innervalue)

    '''for kw in known:
        if(kw[1] == key):
            tokens.append(kw[0])'''
    return tokens

def id2ss(ID):
    #print ID
    #print wn._synset_from_pos_and_offset(str(ID[-1:]), int(ID[:8]))
    return wn._synset_from_pos_and_offset(str(ID[-1:]), int(ID[:8]))

def getSenti(word):
    #print word.name()
    return swn.senti_synset(word.name())

def getSenti_tmp(word):
    return swn.senti_synset(word)
jieba.load_userdict('./mydict.txt')
known = loadWordNet()
stopwords = []
for word in open('./stop_words.txt', 'r'):
    stopwords.append(word.strip())
import os
def handledoc(dir):
    for file in os.listdir(dir):
        filename= dir + file
        words = doSeg(filename)
        n = 0
        p = 0
        for word in words:
            ll = findWordNet(known, word)
            #print word, len(ll)
            if len(ll) != 0:
                n1 = 0.0
                p1 = 0.0
                for wid in ll:
                    desc = id2ss(wid)
                    swninfo = getSenti(desc)
                    #print '*', word, swninfo
                    p1 = p1 + swninfo.pos_score()
                    n1 = n1 + swninfo.neg_score()
        #'''if p1 != 0.0 and n1 != 0.0:
        #    print word, '-> n ', (n1 / len(ll)), " , p ", (p1/len(ll))'''
                p = p + p1 / len(ll)
                n = n + n1 /len(ll)
        print file, " 负面评价: ", n, ", 正面评价: ", p
'''
worddesc = findWordNet(known, u'讨厌')
print len(worddesc)
print type(worddesc)

print getSenti_tmp(id2ss(worddesc[0]).name())'''
import datetime
begin = datetime.datetime.now()
handledoc('/Users/aoyonggang/Downloads/content-2/')
print datetime.datetime.now() - begin