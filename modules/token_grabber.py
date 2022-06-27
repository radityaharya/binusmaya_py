import time
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True
service = Service("geckodriver")

driver = webdriver.Firefox(service=service, options=options)


def login(email: str, password: str):
    try:
        wait = WebDriverWait(driver, 30)
        driver.get("https://newbinusmaya.binus.ac.id")
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(@class,'azure')]"))
        ).click()
        emailInput = wait.until(EC.element_to_be_clickable((By.NAME, "loginfmt")))
        emailInput.send_keys(email)
        driver.find_element(By.XPATH, "//*[@id='idSIButton9']").click()

        passwordinput = wait.until(EC.element_to_be_clickable((By.NAME, "passwd")))
        passwordinput.send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        time.sleep(5)

        token = ""
        for request in driver.requests:
            if request.headers["Authorization"]:
                token = request.headers["Authorization"]
                break
        driver.close()
        driver.quit()
        if token == "":
            raise Exception("Error in getting token")
        return token
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()
        return ""
