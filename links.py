from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd 
import time
import os

class CristianBlueLinks:
    def __init__(self):
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.actions = ActionChains(self.driver)
    
    def land_targeted_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def get_all_links(self):
        results = []
        links = self.driver.find_elements(By.XPATH, '//h2//a')
        for l in links:
            results.append({
                "Category": l.text,
                "Sub Category": "",
                "URL": l.get_attribute('href') 
            })
        else:
            p = pd.DataFrame(results)
            p.to_csv("links.csv", mode='a', header=not os.path.exists("links.csv"), index=False)


bot = CristianBlueLinks()
bot.land_targeted_page('https://christianblue.com/categories/')
time.sleep(5)
bot.get_all_links()