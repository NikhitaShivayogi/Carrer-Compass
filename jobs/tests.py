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
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Exception during tearDown: {e}")

    # Test Case 1: Verify that a user can login successfully
    def test_login(self):
        driver = self.driver
        wait = self.wait

        # Login flow
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("testuser2")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(2)
        self.assertIn("home", driver.page_source.lower())

    # Test Case 2: Verify that user can access the job listings page after login
    def test_job_list(self):
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

    # Test Case 3: Verify that user can apply for the first job listed by clicking the Submit Application button
    def test_apply_for_job_submit_button(self):
        driver = self.driver
        wait = self.wait

        # Login
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("testuser2")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Open job list
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Jobs"))).click()
        time.sleep(2)

        # Click the first job link to open details or application page
        job_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/job/')]")
        if job_links:
            job_links[0].click()
            time.sleep(2)
        else:
            self.fail("No job links found")

        # Click Submit Application button
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit Application')]")))
        submit_button.click()
        time.sleep(2)

        # Verify success message (customize as needed)
        success_message = driver.page_source.lower()
        self.assertIn("application submitted", success_message)

if __name__ == "__main__":
    try:
        unittest.main(
            testRunner=HtmlTestRunner.HTMLTestRunner(
                output='reports',
                report_name="CareerCompassTestReport",
                verbosity=2,
                combine_reports=True,
                add_timestamp=True
            )
        )
    except Exception as e:
        print(f"Exception caught in main: {e}")
