from flask import Flask,render_template
from flask_migrate import Migrate
from reviewapp.model import db,Review,Mobiles

def create_app(): 
    app=Flask(__name__)
    app.config.from_pyfile('config.py')    
    with app.app_context():   
        db.init_app(app)
        migrate = Migrate(app, db)
        

    @app.route("/")
    def hello():
        title="Отзывы на телефоны"
        
        review_list = Review.query.all()
        
        return render_template('index.html',page_title=title,review_list=review_list)
            
    return app
   
            
    
  

