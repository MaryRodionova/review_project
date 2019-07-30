from reviewapp import create_app
from reviewapp.review import get_python_review,get_mobile_all
from reviewapp.sentiment_analys import go
from reviewapp.dostoevsky_analysys import dostoevsky_run

app = create_app()
with app.app_context():
    dostoevsky_run() 
    
   #get_python_review()


