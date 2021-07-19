# eleme-user-s-orders-extraction
*extraction.py* is a python program to extract user's order information on eleme, a popular food delivery platform in China. <br>
This webclawer will log into the user account and write the order information within three months and a week into a csv file.<br>
It is designed to help my classmates Jingyi's econ experiment. 
## Environment
* Compiling environment for **Python 3**
* Python libraries: **selenium, requests, re, unicodecsv**. <br> You can install them with pip easilly. 
* **Chromedriver** matches your chrome browser's version. <br>[Downloading address for chromedriver](http://chromedriver.storage.googleapis.com/index.html). You can also go to the [official website](https://sites.google.com/a/chromium.org/chromedriver/downloads)<br> Detailed instruction for downloading and installation can be found online. Theoretically, other drivers and browsers are also okay as long as they are matched. But I haven't test them yet. 
## A brief manual
Currentlty, this program is able to extract orders within three months and a week as the experiment requires. Detailed information includes the item names, restaurant name, total cost, original price(total), date & time, user's phone number, and the order number. The program will first log into the uesr account, which requires user's phone number and the verification code sent to the phone while logging in. The login process is done by the selenium. Then the driver extract the cookie and transfer it into the form which can be used in requests library. With the cookies, the requests will handle the rest of work. The infromation extracted will be stored as a csv file called *record.csv*. Since we expect to check them by Excel afterwards, the data is encoded by **gbk**. *demo.csv* is uploaded as a demo of extracting results from my own eleme account.<br><br>
After setting the environment, you can run this py file and follow the instructions in the command line. <br><br>
A few points to watch out:<br>
* Change the variable `filename` in line 49 to the real path in your computer where you want store the csv file
* One of the flaws in this program right now is that in the login process, the driver can not locate the login buttom on the page after sending the verification code even though     it initially can. So, remeber to manually click that buttom and wait for the page to load before proceeding to the next step. 
* Make sure that you open the final csv file with gbk encoding format. 
* In convenience of future data analysis, all the information extracted from differnet uesrs will be stored in the same *record.csv*. 
## Other
Initially, we plan to get over the login process by disguising as a mobile device since at that time eleme do not have a login page for PC. We also used selenium to deal with the block-sliding process. However, it did not save us much time and was not very stable. It would fail to pass the detection after 3-4 times of trials. Even though we do not use it anymore, it is still uploaded in the *blocking_sliding.py*. 
