'''
Created by: Tianle Zhu
LastEditTime: 2021-06-14
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import requests
import re
import unicodecsv as ucsv

options = webdriver.ChromeOptions()
#options.add_experimental_option('mobileEmulation',mobileEmulation)
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
options.add_argument("--disable-blink-features=AutomationControlled")

# initialization
driver = webdriver.Chrome(options = options)
wait = WebDriverWait(driver, 10)

# selenium
driver.get("https://h5.ele.me/login/")

cmd = input("enter something as you already logged in ")

driver.refresh()

c = driver.get_cookies()
cookies = {}
# cookie transform
for cookie in c:
    cookies[cookie['name']] = cookie['value']
#print(cookies)
#print(" ")
infoadd = 'https://h5.ele.me/restapi/eus/v1/current_user?info_raw=%7B%7D'
userID =  requests.get(url=infoadd,cookies = cookies).text
# data file
filename = 'c:/python_workspace/src/webclawer/'+userID+'.csv'
f = open(filename,'wb')
w = ucsv.writer(f, encoding = 'gbk')
header = ['item','restaurant','price','time','order number']
w.writerow(header)


url = 'https://h5.ele.me/restapi/bos/v2/users/' + str(userID) + '/orders?limit=200&offset=0'
response = requests.get(url=url, cookies=cookies)
source = response.text

orderPattern = '"alscStoreId".*?,"ClickMore":{"bizParams":'
ingredientPattern = 'ingredient_items":\[\],"name":".*?"'
restaurant_namePattern = 'restaurant_name":".*?"'
timePattern = 'formatted_created_at":".*?","groupDetailUrl"'
costPattern = '"total_amount":.*?,"total_quantity"'
idPattern = '"order_id":".*?","ordertype"'

orders = re.findall(orderPattern,source)
print(len(orders))
for order in orders:
    ingredient = re.findall(ingredientPattern,order)
    item = [i[29:-1] for i in ingredient]
    name = re.findall(restaurant_namePattern,order)[0][18:-1]
    time = re.findall(timePattern,order)[0][23:-19]
    cost = re.findall(costPattern,order)[0][15:-17]
    orderid = re.findall(idPattern,order)[0][12:-13]
    itemstring = ""
    for i in item:
        itemstring += i + "+"
    itemstring = itemstring.replace("➕","+")
    data = [itemstring,name,cost,time,orderid+"\t"]
    w.writerow(data)
    

url2 = 'https://h5.ele.me/restapi/bos/v2/users/' + str(userID) + '/old_orders?limit=8&from_time='
print(url2)

response2 = requests.get(url=url2, cookies=cookies)
print(response2.status_code)
source = response2.text
orders = re.findall(orderPattern,source)
print(len(orders))
for order in orders:
    ingredient = re.findall(ingredientPattern,order)
    item = [i[29:-1] for i in ingredient]
    name = re.findall(restaurant_namePattern,order)[0][18:-1]
    time = re.findall(timePattern,order)[0][23:-19]
    cost = re.findall(costPattern,order)[0][15:-17]
    orderid = re.findall(idPattern,order)[0][12:-13]
    itemstring = ""
    for i in item:
        itemstring += i + "+"
    itemstring = itemstring.replace("➕","+")
    data = [itemstring,name,cost,time,orderid+"\t"]
    w.writerow(data)