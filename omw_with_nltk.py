
# coding: utf-8

# In[1]:


import pandas as pd
import nltk
#nltk.download('omw')
from nltk.corpus import wordnet as wn
from itertools import chain
import sys


# In[2]:


def hypernym_chain(s):
    "calculates the whole hypernym chain for a synset (and its hypernyms) as a list"
    "s: hypernyms() of a synset"
    second = s[0].hypernyms()
    y = []
    chain = []
    ls = len(second)
    if ls >= 1:
        t = s[0].hypernyms()
        y += hypernym_chain(t)
        chain = t+y
        return chain
    else: return chain
    


# In[3]:


# read in mapping data
data = pd.read_table('wn30map31.txt', delimiter='\t', skiprows = 7)
mapp = pd.DataFrame(data)

# convert columns to lists
wn31 = mapp['WordNet 3.1'].tolist()
wn3 = mapp['WordNet 3.0'].tolist()

wn31 = [str(x).zfill(8) for x in wn31]
wn3 = [str(x).zfill(8) for x in wn3]

# read in cili (source: https://lr.soh.ntu.edu.sg/omw/ili)
cili = pd.read_table('cili.tsv')
cili = pd.DataFrame(cili)

iliId = cili['ili_id'].tolist()
iliDef = cili['definition'].tolist()

# map two columns of a list
def f(a,b,c):
    return c[b.index(a)]


# In[4]:


def ciliFromDefinition(chainDef):
    if chainDef in iliDef:
        print('ili-ID: ',f(chainDef,iliDef,iliId))
    else: print('ili-ID: Not in list')


# In[5]:


def offsetFromSynset(chain):
    "returns the offset-IDs for a chain of Synset as a list"
    #lchain = len(chain)
    #for i in range(lchain):
    hyperOffsets = []
    hyperOffsets = str(chain.offset()).zfill(8)
    print('Offset-ID(3.0): ',hyperOffsets)
    print('Offset-ID(3.1): ',f(hyperOffsets,wn3,wn31))
    return hyperOffsets  


# In[6]:


def key_chain(lem):
    "computes all sense-keys for all lemmata in a list"
    "lem: lemmas() of a synset"
    keys = []
    if lem is not None:
        for index in range(len(lem)):
            if lem[index].key() is not None:
                keys = lem[index].key()
                print('Keys: ',keys)
            else: print('Keys: None')
        return keys


# In[7]:


def info_chain(chain, l='eng'):
    "computes all lemmata, their keys and offset-IDs for each level of a hypernym_chain"
    "chain: a hypernym_chain()"
    "l: an omw language"
    for index in range(len(chain)):
        lem = [] 
        lem += chain[index].lemmas(l)
        print('Level '+ str(index+1) + ':')
        print('HyperLemmata: ',lem)
        print('Definition: ' + str(chain[index].definition()))
        #key_chain(lem)
        offsetFromSynset(chain[index])
        ciliFromDefinition(chain[index].definition())


# In[8]:


def omw_lang(w, p=None, l='eng', ln=None):
    "returns information for a word-form in a specific language"
    "w: a word"
    "p: optional part-of-speech"
    "l: an omw language"
    "ln: optional lexname"
    for synset in wn.synsets(w, lang=l, pos=p):
        if synset.lexname() == ln:
            print('Synset: ' + str(synset))
            print('Offset 3.0: ' + str(synset.offset()).zfill(8))
            print('Offset 3.1: ' + f(str(synset.offset()).zfill(8),wn3,wn31))
            ciliFromDefinition(synset.definition())
            print('Type: ' + str(synset.pos()))
            print('LexName: ' + str(synset.lexname()))
            print('Lemmata: ' + str(synset.lemma_names(l)))
            print('Definition: ' + str(synset.definition()))
            print('Examples: ' + str(synset.examples()))
            for hyper in synset.hypernyms():
                chain = hypernym_chain(synset.hypernyms())
                chain.insert(0,hyper)     
                print('Hypernyms: ' + str(chain))
                info_chain(chain,l)
            print('------------------------------------------------------------------------------------------------------------')
        if ln == None:
            print('Synset: ' + str(synset))
            print('Offset 3.0: ' + str(synset.offset()).zfill(8))
            print('Offset 3.1: ' + f(str(synset.offset()).zfill(8),wn3,wn31))
            ciliFromDefinition(synset.definition())
            print('Type: ' + str(synset.pos()))
            print('LexName: ' + str(synset.lexname()))
            print('Lemmata: ' + str(synset.lemma_names(l)))
            print('Definition: ' + str(synset.definition()))
            print('Examples: ' + str(synset.examples()))
            for hyper in synset.hypernyms():
                chain = hypernym_chain(synset.hypernyms())
                chain.insert(0,hyper)
                print('Hypernyms: ' + str(chain))
                info_chain(chain,l)
            print('------------------------------------------------------------------------------------------------------------')


# In[10]:


# Test examples

#spanish words
s=['avanzar', 'mover', 'irse']

#english words
e=['advance', 'move', 'journey']


# In[11]:


# Compare English and Spanish senses and hierarchies:
#sys.stdout = open("SpEng.txt", "w")

for i,(spa,eng) in enumerate(zip(s,e)):
    print('___________________________________________________________________________________________________________________')
    print([i], 'SPANISH ' + spa)
    omw_lang(spa,'v','spa','verb.motion')
    print([i], 'ENGLISH ' + eng)
    omw_lang(eng,'v','eng','verb.motion')
    
#sys.stdout.close()
    


# In[14]:


m=['要','吃']
e=['want', 'eat']


# In[15]:


# it does also work for Mandarin:

for i,(mand,eng) in enumerate(zip(m,e)):
    print('____________________________________________________________________________________________________________________')
    print([i], 'MANDARIN ' + mand)
    omw_lang(mand,'v','cmn')#,'verb.motion')
    print([i], 'ENGLISH ' + eng)
    omw_lang(eng,'v','eng')#,'verb.motion')


# In[16]:


# Example for a NOUN:
omw_lang('air','n', 'eng', ln='noun.location')

