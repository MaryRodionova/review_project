from dostoevsky.tokenization import UDBaselineTokenizer
from dostoevsky.word_vectors import SocialNetworkWordVectores
from dostoevsky.models import SocialNetworkModel
from reviewapp.model import db,Review


from gensim.utils import simple_preprocess
import gensim
from gensim import corpora
from pprint import pprint
import pandas as pd
import numpy as np
import sqlite3




def save_sentiment(mobile_name,mobile_id,title,text,sentiment_new): 
         
    review_review=Review(mobile_name=mobile_name,mobile_id=mobile_id,title=title,text=text,count_words=0,sentiment=sentiment_new)
    db.session.add(review_review)
    db.session.commit()


def dostoevsky_run():        


    result=[]

    with open("reviews.txt", "r", encoding='utf-8') as file:
        my_docs = file.readlines()



    # Tokenize the docs
    tokenized_list = [simple_preprocess(doc) for doc in my_docs]



    tokenizer = UDBaselineTokenizer()
    tokens = tokenizer.split(my_docs)  # [('всё', 'ADJ'), ('очень', 'ADV'), ('плохо', 'ADV')]

    word_vectors_container = SocialNetworkWordVectores()

    vectors = word_vectors_container.get_word_vectors(tokens)
    vectors.shape  # (3, 300) - three words/vectors with dim=300


    model_vec = SocialNetworkModel(
    tokenizer=tokenizer,
    word_vectors_container=word_vectors_container,
    lemmatize=False,
    )


    conn = sqlite3.connect('review.db')
    c = conn.cursor()

    with open('reviews.txt', 'w', encoding='utf-8') as f:
        # Считываем тексты твитов 
        for row in c.execute('SELECT * FROM review'):
            if row[0]:
                rev = row[4]
                idd=row[1]
                
                a = model_vec.predict([rev])  # array(['negative', 'positive'], dtype='<U8')
                
                result.append({
                            "mobile_name": row[1],
                            "mobile_id" : row[2],
                            "title":row[3],
                            "text": row[4],
                            "sentiment": a[0]                            

                        })                       
                              
                
                
    for r in result:
        save_sentiment(r["mobile_name"],r["mobile_id"],r["title"],r["text"],r["sentiment"])
    
    
                

