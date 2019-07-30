from reviewapp.model import db,Review,Mobiles
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras.models import Model
import sqlite3

import logging
import multiprocessing
import gensim
from gensim.models import Word2Vec

def go():
    
   # Считываем данные
    n = ['id', 'date', 'name', 'text', 'typr', 'rep', 'rtw', 'faw', 'stcount', 'foll', 'frien', 'listcount']
    data_positive = pd.read_csv('positive.csv', sep=';', error_bad_lines=False, names=n, usecols=['text'])
    data_negative = pd.read_csv('negative.csv', sep=';', error_bad_lines=False, names=n, usecols=['text'])

    # Формируем сбалансированный датасет
    sample_size = min(data_positive.shape[0], data_negative.shape[0])
    raw_data = np.concatenate((data_positive['text'].values[:sample_size],
                            data_negative['text'].values[:sample_size]), axis=0)
    labels = [1] * sample_size + [0] * sample_size
    


    def preprocess_text(text):
        text = text.lower().replace("ё", "е")
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub('@[^\s]+', 'USER', text)
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        text = text.lower()
        text = re.sub(' на', '', text)
        text = re.sub(' но', '', text)
        text = re.sub(' все', '', text)
        text = re.sub(' в', '', text)
        text = re.sub(' и', '', text)
        text = re.sub(' не', '', text)
        text = re.sub(' по', '', text)
        text = re.sub(' с', '', text)
        text = re.sub(' -', '', text)
        text = re.sub(' а', '', text)
        text = re.sub(' при', '', text)
        text = re.sub(' что', '', text)     
        return text.strip()


    data = [preprocess_text(t) for t in raw_data]


    
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=1)

    #Далее с помощью библиотеки Gensim обучил Word2Vec-модель со следующими параметрами:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



    # Считываем файл с предобработанными твитами
    data_text = gensim.models.word2vec.LineSentence('reviews.txt')
    

    
    # Обучаем модель 
    model = Word2Vec(data_text, size=200, window=5, min_count=1, workers=multiprocessing.cpu_count())
    model.save("model/model.w2v")

