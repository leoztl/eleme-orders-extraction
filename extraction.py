'''
Created by: Tianle Zhu
LastEditTime: 2021-07-19
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
import time as t

def timecal():
    # calculate and return the earliest order timestamp
    month = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    current = t.strftime('%Y-%m-%d',t.localtime())
    y,m,d = current.split("-")
    y = int(y)
    m = int(m)
    d = int(d)
    # minus 7 days
    if d > 7:
        d -= 7
    else:
        if m > 1:
            m -= 1
            d = month(m)-(7-d)
        else:
            y -= 1
            m = 12
            d = month(m)-(7-d)
    #minus 3 months
    if m > 3:
        m -= 3
    else:
        y -=1
        m = 12 - (3-m)
    
    ret = str(y)+"-" + str(m) + "-" + str(d)
    return t.mktime(t.strptime(ret,'%Y-%m-%d'))

standardstamp = timecal()
#--------------extraction part----------------------------------
options = webdriver.ChromeOptions()
#options.add_experimental_option('mobileEmulation',mobileEmulation)
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
options.add_argument("--disable-blink-features=AutomationControlled")

# initialization
driver = webdriver.Chrome(options = options)
wait = WebDriverWait(driver, 60)

# manually log in
driver.get("https://h5.ele.me/login/")
phone = input("user phone number\n")
iframe = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/iframe')))
driver.switch_to.frame(iframe)
driver.find_element_by_name("fm-sms-login-id").send_keys(phone)
driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/form/div[3]/div[2]/a").click()
sleep(0.5)
code = input("your verification message:\n")
driver.find_element_by_name("fm-smscode").send_keys(code)
cmd = input("enter something as you already logged in ")
# get cookie
driver.refresh()
c = driver.get_cookies()
cookies = {}
c = driver.get_cookies()
cookies = {}
driver.quit()

# cookie transform
for cookie in c:
    cookies[cookie['name']] = cookie['value']

# data file
filename = 'c:/python_workspace/src/webclawer/record.csv'
f = open(filename,'wb')
w = ucsv.writer(f, encoding = 'gbk')
header = ['item','restaurant','price','original price','time','phone','order number'] # header of the csv file
w.writerow(header)

# first to get the userID
infoadd = 'https://h5.ele.me/restapi/eus/v1/current_user?info_raw=%7B%7D'
userID =  requests.get(url=infoadd,cookies = cookies).text
#print(cookies)

# then to get the orders
url = 'https://h5.ele.me/restapi/bos/v2/users/' + str(userID) + '/orders?limit=200&offset=0' # orderurl in which the userID is involved
response = requests.get(url=url, cookies=cookies)
source = response.text

# regexes for target info
orderPattern = '"alscStoreId".*?,"ClickMore":{"bizParams":'
itemPattern = 'ingredient_items":\[\],"name":".*?"'
restaurant_namePattern = 'restaurant_name":".*?"'
timePattern = 'formatted_created_at":".*?","groupDetailUrl"'
costPattern = '"total_amount":.*?,"total_quantity"'
idPattern = '"order_id":".*?","ordertype"'
pricePattern1 = '"original_price":.*?,"price":.*?,"quantity"'
pricePattern2 = '"price":.*?"quantity"'

# patterns matching
orders = re.findall(orderPattern,source)
for order in orders:
    ingredient = re.findall(itemPattern,order)
    item = [i[29:-1] for i in ingredient]
    name = re.findall(restaurant_namePattern,order)[0][18:-1]
    time = re.findall(timePattern,order)[0][23:-19]
    cost = re.findall(costPattern,order)[0][15:-17]
    orderid = re.findall(idPattern,order)[0][12:-13]
    result1 = re.findall(pricePattern1,order)
    originalPrice = 0
    for i in result1:
        result2 = re.findall(pricePattern2,i)[0][8:-11]
        originalPrice += float(result2)
    itemstring1 = ""
    for i in item:
        itemstring1 += i + "+"
    itemstring1 = itemstring1.replace("\u2795","+")
    itemstring1 = itemstring1.replace("\u2b50","")
    itemstring2 = ""
    for i in itemstring1:
        if i >= '\u2600' and i<= '\u27bf':
            continue
        else:
            itemstring2 += i
    itemstring2 = itemstring2.replace("\u2b50","")
    data = [itemstring2[:-1],name,cost,originalPrice,time,phone+"\t",orderid+"\t"]
    w.writerow(data)
    
timestampPattern = '"from_time":.*?,"orders"'

timestamp = ""
timelimit = False

while True:
    url = "https://h5.ele.me/restapi/bos/v2/users/"+str(userID)+"/old_orders?limit=8&from_time=" + timestamp
    source = requests.get(url = url, cookies = cookies).text
    sleep(0.5)
    timestamp = re.findall(timestampPattern, source)[0][12:-9]
    orders = re.findall(orderPattern,source)
    for order in orders:
        ingredient = re.findall(itemPattern,order)
        item = [i[29:-1] for i in ingredient]
        name = re.findall(restaurant_namePattern,order)[0][18:-1]
        time = re.findall(timePattern,order)[0][23:-18]
        cost = re.findall(costPattern,order)[0][15:-17]
        orderid = re.findall(idPattern,order)[0][12:-13]
        result1 = re.findall(pricePattern1,order)
        originalPrice = 0
        date = time[0:-6]
        currentstamp =  t.mktime(t.strptime(date,'%Y-%m-%d'))
        if currentstamp < standardstamp:
            timelimit = True
            break
        for i in result1:
            result2 = re.findall(pricePattern2,i)[0][8:-11]
            originalPrice += float(result2)
        itemstring1 = ""
        for i in item:
            itemstring1 += i + "+"
        itemstring1 = itemstring1.replace("\u2795","+")
        itemstring1 = itemstring1.replace("\u2b50","")
        itemstring2 = ""
        for i in itemstring1:
            if i >= '\u2600' and i<= '\u27bf':
                continue
            else:
                itemstring2 += i
        data = [itemstring2[:-1],name,cost,originalPrice,time,phone+"\t",orderid+"\t"]
        w.writerow(data)
    if timelimit:
        break
    if len(orders) == 0:
        break
