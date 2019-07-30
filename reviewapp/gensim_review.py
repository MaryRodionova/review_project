import gensim
from gensim import corpora
from pprint import pprint
import pandas as pd
import numpy as np
import gensim.downloader as api
import matplotlib.pyplot as plt

# Стандартное импортирование plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot

from gensim.utils import simple_preprocess
from smart_open import smart_open
import os
 

from gensim.models.word2vec import Word2Vec
from multiprocessing import cpu_count

# Использование cufflinks в офлайн-режиме
import cufflinks
cufflinks.go_offline()


with open("reviews.txt", "r", encoding='utf-8') as file:
    my_docs = file.readlines()



# Tokenize the docs
tokenized_list = [simple_preprocess(doc) for doc in my_docs]
print(tokenized_list)


# Create the Corpus

"""

# Create gensim dictionary form a single tet file
dictionary = corpora.Dictionary(simple_preprocess(line, deacc=True) for line in open('reviews.txt', encoding='utf-8'))


#print(dictionary.token2id)
mycorpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized_list]
#print(mycorpus)

#print(mycorpus)
word_counts = [[(dictionary[id], count) for id, count in line] for line in mycorpus]
#print(word_counts)

#for items,value in word_counts[0]:
#    print(items,value)


# Настройка глобальной темы cufflinks

cufflinks.set_config_file(world_readable=True, theme='pearl', offline=True)




word_counts[0].value.iplot(
    
   
    x = word_counts[0].value
    # Specify the category
    
    

)


    # Download the models


model = Word2Vec.load('model/model.w2v')

#sim_words = model.wv.most_similar('intelligence')  
vocabulary = model.wv.vocab  
print(vocabulary) 

#sim_words = model.wv.most_similar('экран')  
#print(sim_words)
"""