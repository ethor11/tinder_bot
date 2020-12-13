import selenium
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from secrets import username, password
import selenium.webdriver.support.ui
#from beauty_predict import scores
import requests, os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def download_image(source, destination):
    img_data = requests.get(source).content
    with open(destination, 'wb') as out:
        out.write(img_data)


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome("C:/Users/ethor/OneDrive/Documents/chromedriver/chromedriver.exe")
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.threshold = 6.75
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
        sleep(5)
        init_send_code = self.driver.find_element_by_xpath("//*[@id='u_0_f']")
        init_send_code.click()
        sleep(5)
        send_code = self.driver.find_element_by_xpath("//*[@id='u_0_h']")
        send_code.click()
        sleep(5)
        backout_2fa = self.driver.find_element_by_xpath("//*[@id='facebook']/body/div[3]/div[2]/div/div/div/div[1]/div/div[1]/a")
        backout_2fa.click()
        sleep(15)
        continue_tinder = self.driver.find_element_by_xpath('//*[@id="checkpointSubmitButton"]')
        continue_tinder.click()
        sleep(25)
        #self.driver.switch_to_window(base_window)

    def like(self):
        like = self.driver.find_element_by_xpath("//*[@id='content']/div/div[1]/div/div/main/div/div[1]/div/div[2]/div[4]/button")
        like.click()

    def dislike(self):
        dislike = self.driver.find_element_by_xpath("//*[@id='content']/div/div[1]/div/div/main/div/div[1]/div/div[2]/div[4]/button")
        dislike.click()
    
        def auto_swipe(self):
            while True:
                sleep(0.5)
                try:
                    self.like()
                except Exception:
                    try:
                        self.close_popup()
                    except Exception:
                        self.close_match()

    def choose(self):
        scrs = self.current_scores()
        choice = "DISLIKE"
        if len(scrs) == 0:
            self.dislike()
        elif [scr > self.threshold for scr in scrs] == len(scrs) * [True]:
            self.like() # if there are several faces, they must all have
            choice = "LIKE" # better score than threshold to be liked
        else:
            self.dislike()

        print("Scores : ",
              scrs,
              " | Choice : ",
              choice,
              " | Threshold : ",
              self.threshold)

    def ai_swipe(self):
        while True:
            sleep(3)
            try:
                self.choose()
            except Exception as err:
                try:
                    self.close_popup()
                except Exception:
                    try:
                        self.close_match()
                    except Exception:
                         print("Error: {0}".format(err))


    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def get_image_path(self):
        body = self.driver.find_element_by_xpath('//*[@id="Tinder"]/body')
        bodyHTML = body.get_attribute('innerHTML')
        startMarker = '<div class="Bdrs(8px) Bgz(cv) Bgp(c) StretchedBox" style="background-image: url(&quot;'
        endMarker = '&'

        if not self.begining:
            urlStart = bodyHTML.rfind(startMarker)
            urlStart = bodyHTML[:urlStart].rfind(startMarker)+len(startMarker)
        else:
            urlStart = bodyHTML.rfind(startMarker)+len(startMarker)

        self.begining = False
        urlEnd = bodyHTML.find(endMarker, urlStart)
        return bodyHTML[urlStart:urlEnd]

    def current_scores(self):
        url = self.get_image_path()
        outPath = os.path.join(APP_ROOT, 'images', os.path.basename(url))
        download_image(url, outPath)
        return scores(outPath)


bot = TinderBot()
bot.login()