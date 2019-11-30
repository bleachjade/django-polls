import datetime
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from polls.models import Question,Choice
from django.utils import timezone
from django.contrib.auth.models import User
from seleniumlogin import force_login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (days < 0 for questions published
    in the past, days > 0 for questions published in the future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question

def create_choice(choice_text, question: Question):
    return Choice.objects.create(choice_text=choice_text,question=question)

class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome('C:/Users/Jade/Downloads/chromedriver')
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTestCase, self).tearDown()

    def test_polls_initialize(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get(self.live_server_url + '/polls/')
        #find the form element
        h2 = selenium.find_element_by_tag_name('h2')
        self.assertEqual('Available Polls', h2.text)

    def test_create_question(self):
        selenium = self.selenium
        question = create_question("What is your favourite subject?", days=-1)
        selenium.get(self.live_server_url + '/polls/')
        element = selenium.find_element_by_id(f"question{ question.id }")  
        self.assertEqual(element.text,'What is your favourite subject?')

    def test_create_question_detail(self):
        selenium = self.selenium
        question = create_question("What is your favourite subject?", days=-1)        
        selenium.get(self.live_server_url + '/polls/')
        links = selenium.find_elements_by_tag_name('a')
        links[1].click()
        print(links)
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/polls/' + f"{question.id}/")

    def test_force_login(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + '/accounts/login/')
        user = User.objects.create_user(username='admin', password='password')
        force_login(user, selenium, self.live_server_url)

    def test_create_question_result(self):
        selenium = self.selenium
        question = create_question("What is your favourite subject?", days=-1)
        choice = create_choice("ISP", question)
        username = 'admin'
        password = 'password'
        User.objects.create_user(username='admin', password='password')
        selenium.get(self.live_server_url + '/accounts/login')
        selenium.find_element_by_id("id_username").send_keys(username)
        selenium.find_element_by_id("id_password").send_keys(password)
        selenium.find_element_by_id("submit").click()
        # link = selenium.find_element_by_tag_name('a')
        # print(link)
        # link.click()
        # time.sleep(5)
        wait = WebDriverWait(selenium, 10)
        accept = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "a")))

        actions = ActionChains(selenium)
        actions.move_to_element(accept).click().perform()
        choice1 = selenium.find_element_by_id(f"choice{ choice.id }")
        choice1.click()
        selenium.find_element_by_id("submit_vote").click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/polls/' + f"{question.id}/")
