from datetime import datetime
from reviewapp.model import db,Review,Mobiles
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import socks
import socket
import time



def get_html(url,params):
    #socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    #socket.socket = socks.socksocket
    try:
        result = requests.get(url,params,headers={'User-Agent': UserAgent().chrome})
        #print(result.text)
        #print('*' * 100)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_mobile_all():   
    mobile_all=[]    
    links=[]      
    for i in range(1,4): 

        url="https://market.yandex.ru/catalog--mobilnye-telefony/54726/list"
        params = {
        "hid": "91491", 
        "track": "pieces",   
        "onstock": 1,
        "local-offers-first": 0,
        "how": "opinions",
        "page": i
        }

        html = get_html(url,params=params)
        if html:
            soup = BeautifulSoup(html, 'html.parser')     
            #with open("python-org-news.html", "w",encoding="utf8") as f:
            #    f.write(html)   

            all_mobiles = soup.findAll('div', class_='n-snippet-cell2 i-bem b-zone b-spy-visible n-snippet-cell2_type_product')
            
            for all_mobile in all_mobiles:
                link = all_mobile.find('a',class_='n-snippet-cell2__image link').get('href')
                #a=link.find('/',2)
                #b=link[a+1:50]
                #link_mobile = link.split('/')
                #telefony = link_mobile[2]
                #id_telefony = telefony.split('=')
                #link_id_telefony = id_telefony[0]
                mobile_url = link.split('?')
                
                
                if mobile_url[0] not in links:
                    mobile_name=mobile_url[0].split('/')  

                    save_id(mobile_url[0],mobile_name[1][18:].capitalize(),mobile_name[2])

                    links.append({
                                "url":mobile_url[0],
                                "name":mobile_name[1][18:].capitalize(),
                                "id": mobile_name[2]

                            }) 

    
    return links




def get_python_review():   
    result_review=[]
    mobile_all=Mobiles.query.all()
  

    for mobile in mobile_all:

        for i in range(1,11):            
            
            url="https://market.yandex.ru%s/reviews" % (mobile.mobile_url) 
            params = {
            "hid": "91491",
            "page": i        
            }
            
            print(url)

            html = get_html(url,params=params)
            
            #time.sleep(10)
            if html:
                soup = BeautifulSoup(html, 'html.parser')    
                all_review = soup.findAll('dl', class_='n-product-review-item__stat')               
                
                
                for review in all_review:
                    print(review)
                    try:
        
                        title=review.find('dt',class_='n-product-review-item__title').text
                        text=review.find('dd',class_='n-product-review-item__text').text 
                        mobile_name = mobile.mobile_name
                        mobile_id = mobile.mobile_id

                        save_review(mobile_name,mobile_id,title,text)
                        
           
                        print(mobile_name)
                    except:
                        continue 


                        result_review.append({
                            "mobile_name": mobile.mobile_id,
                            "mobile_id" : mobile.mobile_id,
                            "title":title,
                            "text": text                            

                        })                       
                                        
                    
                
    return result_review
         
def save_id(mobile_url,mobile_name,mobile_id):        
    review_id=Mobiles(mobile_url=mobile_url,mobile_name=mobile_name,mobile_id=mobile_id)
    db.session.add(review_id)
    db.session.commit()


def save_review(mobile_name,mobile_id,title,text): 
    text_exists = Review.query.filter(Review.text == text).count()
    print(text_exists)
    if not text_exists:      
        review_review=Review(mobile_name=mobile_name,mobile_id=mobile_id,title=title,text=text)
        db.session.add(review_review)
        db.session.commit()

#result_review=get_python_news()

#with open('review.csv', 'w', encoding='utf-8', newline='') as f:
#    fields = ['title', 'text_review']
#    writer = csv.DictWriter(f, fields)
#    writer.writeheader()
#    for user in result_review:
#        writer.writerow(user)



