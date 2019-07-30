from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_name = db.Column(db.String, nullable=False)
    mobile_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)
    count_words = db.Column(db.Integer, nullable=True)
    sentiment = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return '<News {} {} {} {} {} {} >'.format(self.mobile_name,self.mobile_id,self.title,self.text,self.count_words,self.sentiment)


class Mobiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_url = db.Column(db.String, nullable=False)
    mobile_name = db.Column(db.String, nullable=False)
    mobile_id = db.Column(db.String, nullable=False)


    def __repr__(self):
        return '<News {} {} {}>'.format(self.mobile_url,self.mobile_name,self.mobile_id)
