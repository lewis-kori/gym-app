import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LoginTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        # create a new Firefox session
        self.driver = webdriver.Chrome('/Users/lewiskori/Downloads/chromedriver')
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("http://127.0.0.1:8000")

    def testLogin(self):
        email_input = self.driver.find_element_by_name('login')
        password_input = self.driver.find_element_by_id('id_password')
        email_input.send_keys('lewistest@test.com')
        password_input.send_keys('123qwerty')
        submit_btn = self.driver.find_element_by_class_name('btn-club')
        submit_btn.click()

    @classmethod
    def tearDown(self) -> None:
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()