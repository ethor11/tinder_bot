import selenium
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from secrets import username, password
#from beauty_predict import scores
import requests, os

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome("C:/Users/ethor/OneDrive/Documents/chromedriver/chromedriver.exe")
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.threshold = 6
        self.beginning = True

    def login(self):
        #Initialize tinder login
        self.driver.get("https://tinder.com/")
        sleep(3)
        login_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button/span')
        login_btn.click()
        sleep(3)
        fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button/span[2]')
        fb_btn.click()

        sleep(1)
        #Login through facebook by swiching login window
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        username_enter = self.driver.find_element_by_xpath("//*[@id='email']")
        username_enter.send_keys(username)

        password_enter = self.driver.find_element_by_xpath("//*[@id='pass']")
        password_enter.send_keys(password)

        sleep(2)

        login_enter = self.driver.find_element_by_xpath("//*[@id='u_0_0']")
        login_enter.click()

        #self.driver.switch_to_window(base_window)

bot = TinderBot()
bot.login()
