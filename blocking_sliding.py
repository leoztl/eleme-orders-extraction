from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep

def get_tracks(distance):
    """
    v = v0+at
    x = v0t+1/2at**2
    """
    tracks = []
    v = 3.5
    t = 1
    mid = distance * 4/5
    current = 0
    while current < distance:
        if mid > current:
            a = 2
        else:
            a = -9
        v0 = v
        x = v0 * t + 1/2*a*t**2
        current += x
        v = v0+a*t
        tracks.append(round(x))
    return tracks


# disguise
mobileEmulation = {
    "deviceMetrics": {"width": 320, "height": 640, "pixelRatio": 3.0},
    "userAgent": 'Mozilla/5.0 (Linux; Android 10; HMA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36'
}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation',mobileEmulation)
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
options.add_argument("--disable-blink-features=AutomationControlled")

# initialization
driver = webdriver.Chrome(options = options)
wait = WebDriverWait(driver, 10)

# change the target phone number here
phoneNum = 00000

# get the web and locate the slide buttom
driver.get("https://h5.ele.me/login/")

phoneBox = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/form/section[1]/input')))
phoneBox.send_keys(phoneNum)
sleep(1)
send_key_buttom = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/form/section[1]/button')
send_key_buttom.click()

slide_buttom = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/form/div[2]/div/div[1]/div/div[3]/div')))

# simulate human sliding
tracks = get_tracks(200)
action = ActionChains(driver)
action.click_and_hold(slide_buttom).perform()
for track in tracks:
    try:
        action.move_by_offset(xoffset=track,yoffset=0).perform()
        sleep(0.1)
    except:
        print("sliding completed")
        break
sleep(0.5)
# login
code = input("please type in the verification code you receive\r\n")
codeBox = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/form/section[2]/input')))
codeBox.send_keys(code)
sleep(0.5)
codeBox.send_keys(Keys.ENTER)