from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd 
import time
import os
import csv

class CristianBlueScraper:
    def __init__(self):
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.actions = ActionChains(self.driver)
        self.soup = None

    def extract_element(self, driver, css_selector, attr="text"):
        try:
            element = driver.select_one(css_selector)
            if attr == "text":
                return element.text
            else:
                return element.get(attr)
        except:
            return ""
    
    def extract_element_by_text(self, driver, tag, string, attr='text'):
        try:
            element = driver.find(tag, string=string)
            if attr == 'text':
                return element.text 
            else:
                return element.get(attr)
        except:
            return ''
    
    def land_targeted_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        try:
            close_add = self.driver.find_element(By.XPATH, '//button[@class="close"]')
            self.driver.implicitly_wait(5)
            self.actions.click(close_add).perform()
        except:
            pass
    
    def handle_pagination(self):
        next_btn = self.driver.find_element(By.XPATH, '//button[@aria-label="Go to next page" and not(contains(@class, "Mui-disabled"))]')
        self.driver.implicitly_wait(3)
        self.actions.click(next_btn).perform()
        time.sleep(1.5)

    def get_all_data(self, cat, sub_cat):
        try:
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            cards = self.soup.select('div[class="category-card"]')
            self.driver.implicitly_wait(5)
            for card in cards:
                data_dict = {}
                data_dict['Category'] = cat
                data_dict['Sub Category'] = sub_cat
                data_dict['Title'] = self.extract_element(driver=card, css_selector="span[class='business-company-name']")
                data_dict['Phone'] = self.extract_element(driver=card, css_selector='a[class="company-phone-no"]', attr="href").replace("tel:", "").strip()
                data_dict['Address'] = self.extract_element(driver=card, css_selector='a[class*="company-add"]')
                data_dict['Direction'] = self.extract_element(driver=card, css_selector='a[class*="company-add"]', attr="href")
                data_dict['Year Advertiser'] = self.extract_element(driver=card, css_selector='p[class*="company-year-advertising"]').strip()
                data_dict['Company Description'] = self.extract_element(driver=card, css_selector='div[class*="company-desc"] > div > p')
                data_dict['Website'] = self.extract_element_by_text(driver=card, tag='a', string='Website', attr="href")
                data_dict['Email'] = self.extract_element_by_text(driver=card, tag='a', string='Email', attr="href").replace("mailto:", "")
                data_dict['Facebook'] = self.extract_element_by_text(driver=card, tag='a', string='Facebook', attr="href")
                data_dict['LinkedIn'] = self.extract_element_by_text(driver=card, tag='a', string='LinkedIn', attr="href")
                data_dict['Instagram'] = self.extract_element_by_text(driver=card, tag='a', string='Instagram', attr="href")
                data_dict['Twitter'] = self.extract_element_by_text(driver=card, tag='a', string='Twitter', attr="href")
                data_dict['Logo'] = self.extract_element(driver=card, css_selector='div[class*="company-logo"] > img', attr="src")
                for key, value in data_dict.items():
                    print(f"{key}: {value}")
                else:    
                    print("-" * 50)
                p = pd.DataFrame([data_dict])
                p.to_csv("BlueCristion.csv", mode='a', header=not os.path.exists("BlueCristion.csv"), index=False)
        except Exception as e:
            print(e)
            print("No cards found")



bot = CristianBlueScraper()
with open("links.csv") as file:
    reader = csv.DictReader(file)
    for r in reader:
        bot.land_targeted_page(r['URL'])
        while True:
            try:
                bot.get_all_data(cat=r['Category'], sub_cat=r['Sub Category'])
                bot.handle_pagination()
            except:
                break
