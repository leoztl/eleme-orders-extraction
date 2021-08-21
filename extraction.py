'''
Created by: Tianle Zhu
LastEditTime: 2021-08-21
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
    #minus 3 months
    if m > 3:
        m -= 3
    else:
        y -=1
        m = 12 - (3-m)
    # minus 7 days
    if d > 7:
        d -= 7
    else:
        if m > 1:
            m -= 1
            d = month[m]-(7-d)
        else:
            y -= 1
            m = 12
            d = month[m]-(7-d)
    
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
f = open(filename,'ab')
w = ucsv.writer(f, encoding = 'gbk')
header = ['item','restaurant','price','original price','time','phone','order number'] # header of the csv file
#w.writerow(header)

# userID
infoadd = 'https://h5.ele.me/restapi/eus/v1/current_user?info_raw=%7B%7D'
userID =  requests.get(url=infoadd,cookies = cookies).text
#print(cookies)

# orders
url = 'https://h5.ele.me/restapi/bos/v2/users/' + str(userID) + '/orders?limit=200&offset=0' # orderurl in which the userID is involved
response = requests.get(url=url, cookies=cookies)
source = response.text

# regexes for target info
orderPattern = '"alscStoreId".*?,"ClickMore":{"bizParams":'
statusPattern = '"status_code":.*?,"status_code_v2"'
discountPattern = '减","price":.*?,"quantity"'
itemPattern = 'ingredient_items":\[\],"name":".*?"'
restaurant_namePattern = 'restaurant_name":".*?"'
timePattern = 'formatted_created_at":".*?","groupDetailUrl"'
costPattern = '"total_amount":.*?,"total_quantity"'
idPattern = '"order_id":".*?","ordertype"'
pricePattern1 = '"original_price":.*?,"price":.*?,"quantity"'
pricePattern2 = '"price":.*?"quantity"'
deliveryfeePattern = '"配送费","price":.*?,"quantity"'
packagefeePattern = '"餐盒","price":.*?,"quantity"'

# patterns matching
offset = 0

while True:
    url = 'https://h5.ele.me/restapi/bos/v2/users/' + str(userID) + '/orders?limit=8&offset=' + str(offset)
    print(url)
    response = requests.get(url=url, cookies=cookies)
    print(response.status_code)
    source = response.text
    orders = re.findall(orderPattern,source)
    print(len(orders))
    for order in orders:
        discount = 0
        discountCollection = re.findall(discountPattern,order)
        deliveryfee = re.findall(deliveryfeePattern,order)[0][14:-11]
        packagefee = re.findall(packagefeePattern,order)
        for i in discountCollection:
            discount += float(i[11:-11])
        if len(packagefee) == 0:
            packagefee = "0.0"
        else:
            packagefee = packagefee[0][13:-11]
        ingredient = re.findall(itemPattern,order)
        status = re.findall(statusPattern,order)[0][14:-16]
        item = [i[29:-1] for i in ingredient]
        name = re.findall(restaurant_namePattern,order)[0][18:-1]
        time = re.findall(timePattern,order)[0][23:-18]
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
    
        detailurl = 'https://h5.ele.me/restapi/bos/v1/users/' + str(userID) + '/orders/' + orderid + '/snapshot'
        response = requests.get(url = detailurl,cookies = cookies)
        print("%s:%s"%(orderid,response.status_code))
        detail = response.text

        descriptionPattern1 = '"deliver_time":".*?","description":".*?","discount_sum"'
        descriptionPattern2 = '"description":".*?","discount_sum"'
        description = re.findall(descriptionPattern1,detail)[0]
        description = re.findall(descriptionPattern2,description)[0][14:-13]
        addressPattern1 = '"address":".*?","alscBizCode"'
        addresssPattern2 = '"address":".*?","avatarAccessURL"'
        try:
            address = re.findall(addressPattern1,detail)[0][11:-15]
        except:
            address = re.findall(addresssPattern2,detail)[0][11:-19]

        data = [itemstring2[:-1],name,cost,discount,originalPrice,time,status,str(phone)+"\t",address,orderid+"\t",description]
        w.writerow(data)

        sleep(0.5)

    offset += 8
    if len(orders) < 8:
        break

    
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
        discount = 0
        discountCollection = re.findall(discountPattern,order)
        deliveryfee = re.findall(deliveryfeePattern,order)[0][14:-11]
        packagefee = re.findall(packagefeePattern,order)
        if len(packagefee) == 0:
            packagefee = "0.0"
        else:
            packagefee = packagefee[0][13:-11]
        for i in discountCollection:
            discount += float(i[11:-11])
        status = re.findall(statusPattern,order)[0][14:-16]
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
        detailurl = 'https://h5.ele.me/restapi/bos/v1/users/' + str(userID) + '/old_orders/' + orderid + '/snapshot'
        response = requests.get(url = detailurl,cookies = cookies)
        sleep(0.5)
        print("%s:%s"%(orderid,response.status_code))
        detail = response.text

        descriptionPattern1 = '"deliver_time":".*?","description":".*?","discount_sum"'
        descriptionPattern2 = '"description":".*?","discount_sum"'
        addressPattern = '"address":".*?","alscBizCode"'
        description = re.findall(descriptionPattern1,detail)[0]
        description = re.findall(descriptionPattern2,description)[0][14:-15]
        address = re.findall(addressPattern,detail)[0][11:-15]
        data = [itemstring2[:-1],name,cost,discount,originalPrice,time,status,str(phone)+"\t",address,orderid+"\t",description]
        w.writerow(data)
    if timelimit:
        break
    if len(orders) == 0:
        break

f.close()
