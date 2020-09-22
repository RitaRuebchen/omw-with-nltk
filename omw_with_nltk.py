
# coding: utf-8

# In[ ]:


#=============================================================
# Title:  Compare two languages with Open Multilingual Wordnet
# Content: functions to calculate the whole hypernym chain, their lemmas and keys
# Author: RitaRuebchen
# Date:   September 2020
#=============================================================


# In[1]:


import nltk
#nltk.download('omw')
from nltk.corpus import wordnet as wn
from itertools import chain


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


def key_chain(lem):
    "computes all sense-keys for all lemmata in a list"
    "lem: lemmas() of a synset"
    keys = []
    if lem is not None:
        for index in range(len(lem)):
            if lem[index].key() is not None:
                #keys = [] 
                keys = lem[index].key()
                print('Keys: ',keys)
            else: print('Keys: None')
        return keys


# In[4]:


def lemmata_chain(chain, l='eng'):
    "computes all lemmata and their keys for each level of a hypernym_chain"
    "chain: a hypernym_chain()"
    "l: an omw language"
    for index in range(len(chain)):
        lem = [] 
        lem += chain[index].lemmas(l)
        print('Level '+ str(index+1) + ':')
        print('HyperLemmata: ',lem)
        key_chain(lem)


# In[5]:


def omw_lang(w, p=None, l='eng', ln=None):
    "returns information for a word-form in a specific language"
    "w: a word"
    "p: optional part-of-speech"
    "l: an omw language"
    "ln: optional lexname"
    for synset in wn.synsets(w, lang=l, pos=p):
        if synset.lexname() == ln:
            print('Synset: ' + str(synset))
            print('Offset: ' + str(synset.offset()))
            print('Type: ' + str(synset.pos()))
            print('LexName: ' + str(synset.lexname()))
            print('Lemmata: ' + str(synset.lemma_names(l)))
            print('Definition: ' + str(synset.definition()))
            print('Examples: ' + str(synset.examples()))
            for hyper in synset.hypernyms():
                chain = hypernym_chain(synset.hypernyms())
                chain.insert(0,hyper)
                print('Hypernyms: ' + str(chain))
                lemmata_chain(chain,l)
            print('------------------------------------------------------------------------------------------------------------')
        if ln == None:
            print('Synset: ' + str(synset))
            print('Offset: ' + str(synset.offset()))
            print('Type: ' + str(synset.pos()))
            print('LexName: ' + str(synset.lexname()))
            print('Lemmata: ' + str(synset.lemma_names(l)))
            print('Definition: ' + str(synset.definition()))
            print('Examples: ' + str(synset.examples()))
            for hyper in synset.hypernyms():
                chain = hypernym_chain(synset.hypernyms())
                chain.insert(0,hyper)
                print('Hypernyms: ' + str(chain))
                lemmata_chain(chain,l)
            print('------------------------------------------------------------------------------------------------------------')


# In[6]:


# Test examples

#spanish words
s=['avanzar', 'mover', 'irse', 'llegar', 'salir', 'subir', 'bajar', 
  'trepar', 'acercarse', 'gatear', 'subir', 'saltarse', 'caerse',
  'pasear', 'llevar', 'seguir', 'perseguir', 'ir_tras', 'salirse',
  'bajarse', 'subirse']

#english words
e=['advance', 'move', 'journey', 'arrive_at', 'bolt_out', 'climb_up',
  'climb_down', 'climb', 'approach', 'crawl_up', 'roll_up',
  'skip_over', 'fall_off', 'cruise_around', 'lead', 'follow',
  'pursue', 'chase', 'hop_off', 'hop_out', 'hop_in']


# In[7]:


# Compare English and Spanish senses and hierarchies:
for i,(spa,eng) in enumerate(zip(s,e)):
    print('____________________________________________________________________________________________________________________')
    print([i], 'SPANISH ' + spa)
    omw_lang(spa,'v','spa','verb.motion')
    print([i], 'ENGLISH ' + eng)
    omw_lang(eng,'v','eng','verb.motion')


# In[8]:


m=['要','吃',' 喝', '拿']
e=['want', 'eat', 'drink', 'take']


# In[9]:


# it does also work for Mandarin:

for i,(mand,eng) in enumerate(zip(m,e)):
    print('____________________________________________________________________________________________________________________')
    print([i], 'MANDARIN ' + mand)
    omw_lang(mand,'v','cmn')#,'verb.motion')
    print([i], 'ENGLISH ' + eng)
    omw_lang(eng,'v','eng')#,'verb.motion')


# In[10]:


# Example for a NOUN:
omw_lang('air','n', 'eng', ln='noun.location')

