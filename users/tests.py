# Generated by Selenium IDE
from django.test import TestCase, Client, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from .models import Profile, Report
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path

class TestLoginpage(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'Testing123!'

        # Set up browser
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1936, 1056)

        # Create account
        user = User.objects.create_user(self.username, f'{self.username}@email.com', self.password)

    def tearDown(self):
        self.driver.quit()

    def test_loginpage(self):

        # Go to login page
        self.driver.find_element_by_link_text('Login').click()
        self.driver.implicitly_wait(0.1)

        # Test that the created user exists
        try:
            user_obj = Profile.objects.get(user__username=self.username)
        except Profile.DoesNotExist:
            user_obj = None
        self.assertIsNotNone(user_obj)
        
        # Test that the user is not logged in (there should not be a log out button)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(By.LINK_TEXT, "Log Out")

        # Enter and submit login credentials to log in
        self.driver.find_element(By.ID, "id_username").send_keys(self.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        
        self.driver.implicitly_wait(0.1)

        # Test that the user is logged in (there should not be a login or register button)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Login')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Register')

        # Log out
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()
        self.driver.implicitly_wait(0.1)

        # Test that the user is not logged in (there should not be a log out button)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log Out')



class TestRegistrationTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_registrationTest(self):
        # Test name: Registration-Test
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get("http://127.0.0.1:8000/")
        # 2 | setWindowSize | 1050x852 |
        self.driver.set_window_size(1050, 852)
        # 3 | click | linkText=Register |
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        # 4 | type | id=id_username | RegisterUser1
        self.driver.find_element(By.ID, "id_username").send_keys("RegisterUser1")
        # 5 | type | id=id_password1 | Checken1234
        self.driver.find_element(By.ID, "id_password1").send_keys("Checken1234")
        # 6 | type | id=id_password2 | Chicken1234
        self.driver.find_element(By.ID, "id_password2").send_keys("Chicken1234")
        # 7 | click | css=.btn |
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        # 8 | click | id=id_password1 |
        self.driver.find_element(By.ID, "id_password1").click()
        # 9 | type | id=id_password1 | Chicken1234
        self.driver.find_element(By.ID, "id_password1").send_keys("Chicken1234")
        # 10 | type | id=id_password2 | Chicken1234
        self.driver.find_element(By.ID, "id_password2").send_keys("Chicken1234")
        # 11 | sendKeys | id=id_password2 | ${KEY_ENTER}
        self.driver.find_element(By.ID, "id_password2").send_keys(Keys.ENTER)
        # 12 | click | linkText=Login |
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        # 13 | click | css=.col-lg-6 |
        self.driver.find_element(By.CSS_SELECTOR, ".col-lg-6").click()
        # 14 | type | id=id_username | RegisterUser1
        self.driver.find_element(By.ID, "id_username").send_keys("RegisterUser1")
        # 15 | click | css=.content-section |
        self.driver.find_element(By.CSS_SELECTOR, ".content-section").click()
        # 16 | type | id=id_password | Chicken1234
        self.driver.find_element(By.ID, "id_password").send_keys("Chicken1234")
        # 17 | click | css=.btn |
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

# Force DEBUG=True to prevent 500 server error (not sure why)
@override_settings(DEBUG=True)
class TestReportSystem(StaticLiveServerTestCase):
    def setUp(self):
        """
        Set up test environment (run once per test function)
        """
        # Inherit setUp()
        super().setUp()
        
        # Set up Chrome web driver and test client
        self.client = Client()
        self.driver = WebDriver(executable_path=binary_path)
        self.driver.implicitly_wait(5)
        
        # Define variables
        self.username = 'testuser'
        self.report_username = 'badguy'
        self.password = 'Testing123!'
        self.report_message = 'This guy is bad! Look at his name!!'

        # Create account
        self.user = User.objects.create_user(username=self.username,
                                        email=f'{self.username}@email.com',
                                        password=self.password)
        
        # Create account of user to be reported
        self.report_user = User.objects.create_user(self.report_username,
                                        f'{self.report_username}@email.com',
                                        self.password)
        
        self.driver.set_window_size(1936, 1056)
        
    def tearDown(self):
        """
        Destroy test environment (run once per test function)
        """
        # Inherit tearDown()
        super().tearDown()
        self.driver.quit()

    def test_report(self):
        """
        Test the report feature
        """
        # Go to login page
        self.driver.get(f"{self.live_server_url}/login/")
        
        # Enter and submit login credentials to log in
        self.driver.find_element(By.ID, "id_username").send_keys(self.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        
        # Go to report badguy user
        # NOTE: this will redirect to login if user is not logged in!
        self.driver.get(f"{self.live_server_url}/report/?user={self.report_user}")
        
        # Check for correct form title
        form_title = self.driver.find_element(By.TAG_NAME, "legend").text
        self.assertEqual(form_title, f"Report {self.report_username}")
        
        # Submit report with given message
        self.driver.find_element(By.ID, "id_message").send_keys(self.report_message)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        
        # Check the correctness of the report object
        report_exists = Report.objects.filter(author=self.user,
                                              reported_user=self.report_user,
                                              message=self.report_message).exists()
        self.assertTrue(report_exists)
