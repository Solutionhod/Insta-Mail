from os import system, name
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

import config
import csv
import json
import random


class Clear:
    """This class clear the console screen by matching the name of the operating system dependent module to give different output on different interpreters, such as windows, mac and linux"""

    def __init__(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')


class WebBrowser:
    """Creating the web driver class"""

    def __init__(self):
        self.timeout = 5
        self.proxy = random.choice(config.ips)
        self.url1 = 'https://www.instagram.com/'
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = self.create_driver()
        self.actions = ActionChains(self.driver)
        self.driver.delete_all_cookies()
        self.driver.get(self.url1)

    def create_options(self):
        """Create Chrome browser options"""
        arg_window_size = '--window-size=1000,650'
        # self.chrome_options.add_argument(f"--proxy-server={self.proxy}")
        self.chrome_options.add_argument(arg_window_size)
        self.chrome_options.add_argument('start-maximized')
        self.chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        self.chrome_options.add_experimental_option(
            'useAutomationExtension', False)
        return self.chrome_options

    def create_driver(self):
        self.create_options()
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=self.chrome_options)
        stealth(driver,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/83.0.4103.53 Safari/537.36',
                languages=['en-US', 'en'],
                vendor='Google Inc.',
                platform='Win32',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=False,
                run_on_insecure_origins=False,
                )
        return driver

    def quit(self):
        self.driver.quit()

    def not_now1(self):
        # Save login info
        sleep(2)
        try:
            self.driver.find_element(
                By.XPATH, "//button[@class='_acan _acao _acas _aj1-']").click()
        except:
            pass

    def not_now2(self):
        # Turn on Notifications
        sleep(2)
        try:
            self.driver.find_element(
                By.XPATH, "//button[@class='_a9-- _a9_1']").click()
        except:
            pass


class Scrape(WebBrowser):
    """Takes inputs of whose account you want to scrape, number of accounts to scrape and scraping options"""

    def __init__(self, target_profile, num_to_scrape):
        super().__init__()
        self.target_profile = target_profile
        self.num_to_scrape = num_to_scrape
        self.user = config.ig_username
        self.pw = config.ig_password
        self.url2 = 'https://www.instagram.com/{}/'
        self.url3 = 'https://instagram.com/{}/?__a=1&__d=dis'
        self.limit = 0
        self.loaded = 0
        self.usernames = []
        self.output = {}
        self.output_list = []
        self.filename = 'data_file.csv'

    def login(self):
        """Send username and password config vars to login form fields and press login button"""
        print(f"Attempting: {self.driver.current_url}")
        user_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((
                By.XPATH, "//input[@name='username']")))
        pass_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((
                By.XPATH, "//input[@name='password']")))
        user_element.send_keys(self.user)
        pass_element.send_keys(self.pw)
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((
                By.XPATH, "//button[@type='submit']")))
        try:
            save_login_info = self.driver.find_element(
                By.XPATH, "//label[@class='_aahb _aahc']")
            if len(save_login_info) > 0:
                save_login_info[0].click()
        except NoSuchElementException:
            pass
        login_button.click()
        sleep(2)
        self.not_now1()
        self.not_now2()
        return self.driver

    def search(self):
        try:
            search_button = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((
                    By.XPATH, "//a[@href='#']")))
            search_button.click()
            sleep(2)
            search_input = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((
                    By.XPATH, "//input[@class='_aauy'] | //input[@placeholder='Search']")))
            search_input.send_keys(self.target_profile)
            sleep(self.timeout)
            for _ in range(3):
                search_input.send_keys(Keys.ENTER)
                sleep(2)
                if self.driver.current_url == self.url2.format(self.target_profile):
                    return self.driver
        except TimeoutException:
            self.driver.get(self.url2.format(self.target_profile))
            print(f"Attempting: {self.driver.current_url}")

    def followers(self):
        followers_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((
                By.XPATH, "//a[contains(@href, '/followers')]")))
        followers_element.click()
        sleep(self.timeout)
        print(f"[Info] - Scraping {self.target_profile} followers...")
        followers = self.driver.find_elements(
            By.CLASS_NAME, '_ab8y')
        is_on = True
        while is_on:
            self.loaded = len(followers)
            scroll_into_view = followers[self.loaded-1]
            scroll_into_view.location_once_scrolled_into_view
            sleep(self.timeout)
            self.driver.implicitly_wait(2)
            followers = self.driver.find_elements(
                By.CLASS_NAME, '_ab8y')
            print(f"Loaded followers: {len(followers)}")
            if self.loaded < len(followers):
                is_on
            else:
                is_on = False
            is_on
        print(f"Successfully loaded {self.loaded} followers usernames")
        for follower in followers:
            self.usernames.append(follower.text)
        print(self.usernames)
        return self.usernames

    def following(self):
        following_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((
                By.XPATH, "//a[contains(@href, '/following')]")))
        following_element.click()
        sleep(self.timeout)
        print(f"[Info] - Scraping {self.target_profile} following...")
        following = self.driver.find_elements(
            By.XPATH, "//div[@class=' _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']")
        is_on = True
        while is_on:
            self.loaded = len(following)
            scroll_into_view = following[self.loaded - 1]
            scroll_into_view.location_once_scrolled_into_view
            sleep(self.timeout)
            self.driver.implicitly_wait(2)
            following = self.driver.find_elements(
                By.XPATH,
                "//div[@class=' _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']")
            print(f"Loaded following: {len(following)}")
            if self.loaded < len(following):
                is_on
            else:
                is_on = False
            is_on
        print(f"Successfully loaded {self.loaded} following usernames")
        for follow in following:
            follow_text = follow.text
            if '\nVerified' in follow_text:
                self.usernames.append(follow_text.replace('\nVerified', ''))
            else:
                self.usernames.append(follow_text)
        print(self.usernames)
        return self.usernames

    def scrape_data(self):
        list(set(self.usernames))
        for username in self.usernames:
            self.driver.get(self.url3.format(username))
            print(f"Attempting: {self.driver.current_url}")
            response_body = self.driver.find_element(
                By.TAG_NAME, 'body').text
            data_json = json.loads(response_body)
            user_data = data_json['graphql']['user']
            is_business = data_json['graphql']['user']['is_business_account']
            if self.limit >= self.num_to_scrape:
                self.quit()
                print("You've reached your scraping limit")
                break
            elif is_business == True and self.limit < self.num_to_scrape:
                self.output_list.append(self.parse_data(user_data))
                self.limit += 1
            else:
                continue
        self.output_file(self.output_list)
        Clear()
        print(
            f"[DONE] - Saved {len(self.output_list)} users info in {self.filename} file!")

    def parse_data(self, user_data):
        try:
            self.output = {
                'User Name': user_data['username'],
                'Full Name': user_data['full_name'],
                'Public Email': user_data['business_email'],
                'Followers Count': user_data['edge_followed_by']['count'],
                'Following Count': user_data['edge_follow']['count'],
                'Is Business': user_data['is_business_account'],
                'Is Verified': user_data['is_verified'],
            }
        except json.decoder.JSONDecodeError:
            print("There was a problem accessing the user data.")
        finally:
            return self.output

    def output_file(self, dict_list):
        fields = ['User Name', 'Full Name', 'Public Email',
                  'Followers Count', 'Following Count', 'Is Business', 'Is Verified']
        with open(self.filename, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(dict_list)
