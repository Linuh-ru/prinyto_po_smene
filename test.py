# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

#Войти в хром
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
driver.implicitly_wait(0.5)


#Стартовая страница (аутентификация)
driver.get("http://tasks.o2dc.ru/login.php")
username = driver.find_element(by=By.NAME, value="username")
username.send_keys("aomarov")
password = driver.find_element(by=By.NAME, value="password")
password.send_keys("qQ12345")
password.send_keys(Keys.ENTER)

def ticket_scanner():
    list_tickets = driver.find_elements(By.CSS_SELECTOR, 'a[class="ticket_selector_nt"]')
    return list_tickets
#Подгрузить список тикетов
driver.implicitly_wait(10)
actual = driver.find_element(By.CSS_SELECTOR, 'li[data-filterid="847"]')
driver.execute_script("arguments[0].scrollIntoView();", actual)
actual.click()
list = []
flag = True
while flag:
    try:
        list_tickets = ticket_scanner()
        for tag in list_tickets:
            list.append(tag.text[3::])
        print(list)
        if len(list) > 0:
            flag = False
        else:
            time.sleep(1)
            actual = driver.find_element(By.CSS_SELECTOR, 'li[data-filterid="847"]')
            driver.execute_script("arguments[0].scrollIntoView();", actual)
            actual.click()
            time.sleep(1)
    except:pass
    time.sleep(1)


#Если понадобится ввести список тикетов вручную
#list = ['117549', '120351', '124679', '125470', '125519', '125515', '125001', '124676']
#Есил нужно пропустить какое то колличество тикетов (например, если уже отписался в них)
list = list[7::]

#Зайти в каждый тикет подставить принято и нажать кнопку отправить
for ticket in list:
    driver.implicitly_wait(10)
    driver.get(f"http://tasks.o2dc.ru/ticket/{ticket}/")
    time.sleep(5)
    #WebDriverWait(driver, 30).until(expected_conditions.visibility_of(driver.find_element(By.CSS_SELECTOR, 'div[class="row"]')))
    WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, 'button[id="BtnQActSubmit"]')))
    #WebDriverWait(driver, 30).until(expected_conditions.invisibility_of_element(driver.find_element(By.CSS_SELECTOR, 'div[class="ibox-content sk-loading"]')))
    time.sleep(15)
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea[id="QActPostText"]')
    # driver.execute_script("arguments[0].scrollIntoView();", actual) #закоментил, потому что правильный скролить не по кномке а по полю ввода текста
    driver.execute_script("arguments[0].scrollIntoView();", textarea)
    textarea.send_keys("Принято по смене")
    actual = driver.find_element(By.CSS_SELECTOR, 'button[id="BtnQActSubmit"]')
    actual.click()
    time.sleep(1)

#driver.find_element_by_css_selector("form[id^='BtnQActSubmit']").click()