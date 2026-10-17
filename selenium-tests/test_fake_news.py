"""Browser smoke test. Start the app first, then run this with Selenium installed."""
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("APP_URL", "http://localhost:8081")

class FakeNewsAgentBrowserTest(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()

    def test_home_page_and_empty_input_validation(self):
        self.driver.get(BASE_URL)
        self.assertIn("Fake News Detection", self.driver.title)
        self.driver.find_element(By.ID, "submit").click()
        result = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )
        self.assertTrue(result.text)

if __name__ == "__main__":
    unittest.main()
