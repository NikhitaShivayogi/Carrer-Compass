import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import HtmlTestRunner 
class CareerCompassTests(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:8000/")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_01_login(self):
        driver = self.driver
        wait = self.wait

        # Login flow
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("testuser2")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait and check
        time.sleep(2)
        self.assertIn("home", driver.page_source.lower())

    def test_02_job_list(self):
        driver = self.driver
        wait = self.wait

        # Login first
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("testuser2")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Go to job list
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Jobs"))).click()
        time.sleep(2)
        print("Current URL after clicking Jobs:", driver.current_url)
        self.assertIn("jobs", driver.page_source.lower())

   
    



    


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))





