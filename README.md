# eleme-user-s-orders-extraction
*eleme_order_info.py* is a python program to extract user's order information on eleme, a popular food delivery platform in China. <br>
This webclawer will log into the user account and write the order information within three months into a csv file.<br>
It is designed to help my classmates Jingyi's econ experiment. 
## environment
* Compiling environment for Python 3
* Python libraries: selenium, requests, re, unicodecsv. 
* chromedriver matches your chrome browser's version. [downloading address for chromedriver](http://chromedriver.storage.googleapis.com/index.html)<br> Detailed instruction for     downloading and installation can be found online. Theoretically, other drivers and browsers are also okay as long as they are matched. But I haven't test them yet. 
## a brief manual
Currentlty, this program is able to extract orders within three months as the experiment requires. Detailed information includes the item names, restaurant name, total cost, original price(total), date & time, and order number. The infromation extracted will be stored as a csv file. Since we expect to check them by Excel afterwards, the data is encoded by gbk. <br>
a few points to watch out:<br>
* change the variable `filename` in line ? to the actual path in your computer where you want store the csv file
* one of the flaws in this program right now is that in the login process, the driver can not locate the login buttom on the page even though it can initially. So, remeber to       manually click that buttom. 
