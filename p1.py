import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import datetime
import os 
import time

url =str(input("enter product url you want to track:\n"))
buy_price=int(input("enter at what price you want to buy this product:\n"))
r_email=str(input("enter your email id:\n"))              
headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

def check_price():
    page = requests.get(url, headers=headers)
    bs= BeautifulSoup(page.content,'html.parser')

    #print(bs.prettify().encode("utf-8"))

    product_title=bs.find(id='productTitle').get_text()
    print(product_title.strip())

    price=bs.find('span',class_='a-price-whole').get_text()
    print(price)

    price_float=float(price.replace(",",""))
    print(price_float)
    file_exists=True
    if not os.path.exists("./price.csv"):
        file_exists=False
    
    with open("price.csv","a") as file:
        writer=csv.writer(file,lineterminator='\n')
        fields=["Timestamp","Price(INR)"]
        if not file_exists:
            writer.writerow(fields)
        timestamp=f"{datetime.datetime.date(datetime.datetime.now())},{datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp,price_float])
        print("wrote data in csv")
    return price_float

def send_email():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("meetraval999@gmail.com","your password")
    subject="price is down"
    body= "place your order now price is in our budget now:",url
    msg=f"Subject:{subject}\n\n\n{body}"
    server.sendmail("meetraval999@gmail.com",r_email,msg)
    print("email is sent!")
    server.quit()
while True:
    price=check_price()
    if(buy_price>price):
        send_email()
        break
    time.sleep(10)
        
        
