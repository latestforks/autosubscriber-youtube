import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    UnexpectedAlertPresentException, ElementNotInteractableException, ElementClickInterceptedException, \
    NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import logging
import os

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def get_clear_browsing_button(driver: webdriver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page.
    Args:
    - driver (webdriver): webdriver parameter.

    Returns:
    - WebElement: returns "* /deep/ #clearBrowsingDataConfirm" WebElement.
    """
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver: webdriver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance.
    Args:
    - driver (webdriver): webdriver parameter.
    - timeout (int): Parameter to stop program after reaches timeout.

    """

    driver.get('chrome://settings/clearBrowserData')
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)
    get_clear_browsing_button(driver).click()
    wait.until_not(get_clear_browsing_button)


def set_driver_opt(req_dict: dict,
                   is_headless=True,
                   website=""):
    """Set driver options for chrome or firefox
    Args:
    - req_dict(dict): dictionary object of required parameters
    - is_headless(bool): bool parameter to check for chrome headless or not
    - website (string): string parameter to enable extensions corresponding to the Website.
    Returns:
    - webdriver: returns driver with options already added to it.
    """
    # Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    if is_headless:
        chrome_options.add_argument('--headless')
    else:
        pass
    chrome_options.add_argument('--user-agent=' + req_dict['yt_useragent'])
    if website != "":
        pass
    else:
        chrome_options.add_argument("--disable-extensions")
        prefs = {"profile.managed_default_content_settings.images": 2, "disk-cache-size": 4096}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        pass
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("disable-infobars")
    if website == "ytmonster":
        pass
    else:
        chrome_options.add_argument("--window-size=1920x1080")
        pass
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    return driver


def google_login(driver: webdriver,
                 req_dict: dict,
                 has_sign_in_btn=True):
    """ Logins to Google with given credentials.
    Args:
    - driver(webdriver): webdriver parameter.
    - req_dict(dict): dictionary object of required parameters
    - has_sign_in_btn (bool): bool parameter to check if page has sign_in_button
    """
    if has_sign_in_btn:
        sign_in_button = driver.find_element_by_css_selector("#buttons > ytd-button-renderer > a")
        ActionChains(driver).move_to_element(sign_in_button).perform()
        sign_in_button.click()
    driver.save_screenshot("screenshots/screenshot.png")
    time.sleep(3)
    email_area = driver.find_element_by_id("identifierId")
    email_area.send_keys(req_dict['yt_email'])
    driver.find_element_by_css_selector("#identifierNext > div > button").click()
    time.sleep(3)
    # print(driver.find_element_by_xpath("/html/body").text)
    pw_area = driver.find_element_by_css_selector("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
    pw_area.send_keys(req_dict['yt_pw'])
    time.sleep(2)
    driver.find_element_by_css_selector("#passwordNext > div > button").click()
    time.sleep(2)
    driver.save_screenshot("screenshots/screenshot.png")


def type_1_for_loop_like_and_sub(driver: webdriver,
                                 d: str,
                                 req_dict: dict,
                                 special_condition=1,
                                 confirm_btn="#likeSub3 > a",
                                 subscribe_btn="#likeSub2 > i"
                                 ):
    """Loop for like and sub, includes google login"""
    i = 0

    def sc_0():
        return driver.switch_to_frame(0)

    def sc_1():
        return driver.switch_to.default_content()

    def sc_2():
        return driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])

    def sc_3():
        return driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
    sc = {
        0: sc_0,
        1: sc_1,
        2: sc_2,
        3: sc_3
    }

    for _ in range(0, 100000000):
        window_before = driver.window_handles[0]
        driver.switch_to_window(window_before)
        driver.switch_to_default_content()
        sc[special_condition]()
        try:
            while driver.find_element_by_id("seconds").text == "0":
                continue
        except (StaleElementReferenceException, NoSuchElementException):
            try:
                time.sleep(1.25)
                while driver.find_element_by_id("seconds").text == "0":
                    continue
            except NoSuchElementException:
                driver.save_screenshot("screenshots/screenshot.png")
                if driver.find_elements_by_id("remainingHint") == 0:
                    driver.quit()
                    return
                else:
                    pass
        try:
            # remaining_videos = driver.find_element_by_id("remainingHint").text
            remaining_videos = driver.find_element_by_xpath("/html/body/div[1]/section/div/"
                                                            "div/div/div/div/div[2]/div[1]/h2/span/div").text
            logging.info(d+" Remaining Videos: " + remaining_videos)
        except NoSuchElementException:
            driver.save_screenshot("screenshots/screenshot.png")
            driver.quit()
            return
        if i == 0:
            confirm_seconds = driver.find_elements_by_id("seconds")[1].text
        driver.switch_to_window(window_before)
        sc[special_condition]()
        driver.save_screenshot("screenshots/screenshot.png")
        try:
            # button_subscribe = driver.find_element_by_css_selector(subscribe_btn)
            button_subscribe = driver.find_elements_by_class_name('btn-step')[0]
            ActionChains(driver).move_to_element(button_subscribe).click().perform()
        except NoSuchElementException:
            logging.info(d+" Couldn't find subscribe_btn")
            break
        # if driver.find_element_by_id("remainingHint").text == "-":
        #     logging.info(d+" Website is not working properly, closing driver")
        #     driver.quit()
        #     return
        if driver.find_element_by_xpath("/html/body/div[1]/section/div/"
                                        "div/div/div/div/div[2]/div[1]/h2/span/div").text == "-":
            logging.info(d+" Website is not working properly, closing driver")
            driver.quit()
            return
        time.sleep(3)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        time.sleep(5)
        try:
            if len(driver.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                    and len(driver.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                          "ytd-toggle-button-renderer[1]")) > 0:
                if i == 0:
                    i += 1
                    google_login(driver, req_dict)
                if len(driver.find_elements_by_css_selector(
                        "#top-level-buttons > ytd-toggle-button-renderer."
                        "style-scope." "ytd-menu-renderer.force-icon-button"
                        ".style-default-active")) > 0:
                    pass
                else:
                    time.sleep(2)
                    driver.execute_script("document.querySelector('#top-level-buttons >"
                                          " ytd-toggle-button-renderer:nth-child(1)').click()")
                time.sleep(2)
                driver.execute_script("document.querySelector('#subscribe-button >"
                                      " ytd-subscribe-button-renderer').click()")
                driver.save_screenshot("screenshots/screenshot_proof.png")
            else:
                driver.switch_to.window(window_before)
                sc[special_condition]()
                while confirm_seconds == "0":  # noqa
                    time.sleep(1.25)
                # button_confirm = driver.find_element_by_css_selector(confirm_btn)
                # button_confirm.send_keys(Keys.ENTER)
                button_confirm = driver.find_elements_by_class_name('btn-step')[2]
                ActionChains(driver).move_to_element(button_confirm).click().perform()
                continue
        except TimeoutException:
            driver.switch_to.window(window_before)
            sc[special_condition]()
            while confirm_seconds == "0":  # noqa
                time.sleep(1.25)
            # button_confirm = driver.find_element_by_css_selector(confirm_btn)
            # button_confirm.send_keys(Keys.ENTER)
            button_confirm = driver.find_elements_by_class_name('btn-step')[2]
            ActionChains(driver).move_to_element(button_confirm).click().perform()
            continue
        driver.switch_to.window(window_before)
        driver.switch_to_default_content()
        sc[special_condition]()
        driver.save_screenshot("screenshots/screenshot.png")
        while confirm_seconds == "0":
            time.sleep(1.25)
        try:
            try:
                # WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.CSS_SELECTOR, confirm_btn)))
                button_confirm = driver.find_elements_by_class_name('btn-step')[2]
                WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.CLASS_NAME, button_confirm)))
            except TimeoutException:
                pass
            # driver.execute_script("document.querySelector('#likeSub3 > a').click()")
            button_confirm = driver.find_elements_by_class_name('btn-step')[2]
            ActionChains(driver).move_to_element(button_confirm).click().perform()
            continue
        except NoSuchElementException:
            time.sleep(1.25)
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            driver.close()
            driver.switch_to.window(window_before)
            continue


def subpals_functions(req_dict: dict):
    """subpals login and activate free plan then call outer subscribe loop function(for_loop_like_and_sub)"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.get("https://www.subpals.com/login/final/" + req_dict['yt_channel_id'] + "/")  # Type_1
    driver.implicitly_wait(20)
    driver.save_screenshot("screenshots/screenshot.png")
    pw_place = driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div >"
                                                   " form > div:nth-child(2) > input")
    pw_place.send_keys(req_dict['pw_subpals'])
    time.sleep(3)
    driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div > form > button") \
        .send_keys(Keys.ENTER)

    driver.switch_to.default_content()
    if len(driver.find_elements_by_partial_link_text("Activated")) > 0:
        driver.quit()
        return
    driver.execute_script("window.scrollTo(0, 300);")
    try:
        driver.find_element_by_xpath("#core-wrapper > section > div > div > div > div > div >" 
                                     " div.userContent_pricing > div:nth-child(2) >" 
                                     " div:nth-child(1) > div > div.panel-body > div.btn-holder > form > a") \
            .send_keys(Keys.ENTER)
        time.sleep(1.25)
    except NoSuchElementException:
        logging.info("subpals activate button passed 1")
        pass
    try:
        activate_btn = driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div >"
                                                           " div.userContent_pricing > div:nth-child(2) >"
                                                           " div:nth-child(1) > div > div.panel-body > "
                                                           "div.btn-holder > form > a")
        ActionChains(driver).move_to_element(activate_btn).perform()
        activate_btn.click()

    except NoSuchElementException:
        logging.info("subpals activate button passed 2")
        pass
    driver.save_screenshot("screenshots/screenshot.png")
    driver.switch_to.default_content()
    type_1_for_loop_like_and_sub(driver,
                                 "subpals",
                                 req_dict
                                 )
    driver.quit()


def ytpals_functions(req_dict: dict):
    """ytpals login and activate free plan then call outer subscribe loop function(for_loop_like_and_sub)"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.get("https://www.ytpals.com/login/final/" + req_dict['yt_channel_id'] + "/")  # Type_1
    driver.implicitly_wait(20)
    driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div >"
                                        " form > div:nth-child(2) > input").send_keys(req_dict['pw_ytpals'])
    driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div > form > button").click()
    if len(driver.find_elements_by_partial_link_text("Activated")) > 0:
        driver.quit()
        return
    driver.execute_script("window.scrollTo(0, 300);")
    try:
        driver.find_element_by_xpath("//*[@id='core-wrapper']/section/div/div/div[2]/div/div/div[2]/div[2]/"
                                     "div[1]/div/div[2]/div[2]/form/a") \
            .send_keys(Keys.ENTER)
    except NoSuchElementException:
        logging.info("ytpals activate button passed 1")
        pass
    try:
        activate_btn = driver.find_element_by_css_selector("#core-wrapper > section > div > div > div:nth-child(2) >"
                                                           " div > div > div.userContent_pricing > div:nth-child(2) >"
                                                           " div:nth-child(1) > div > div.panel-body > div.btn-holder >"
                                                           " form > a")
        ActionChains(driver).move_to_element(activate_btn).perform()
        activate_btn.click()

    except NoSuchElementException:
        logging.info("ytpals activate button passed 2")
        pass
    driver.save_screenshot("screenshots/screenshot.png")
    driver.switch_to.default_content()
    type_1_for_loop_like_and_sub(driver,
                                 "ytpals",
                                 req_dict)
    driver.quit()


def sonuker_functions(req_dict: dict):
    """sonuker login and activate free plan then call outer subscribe loop function(for_loop_like_and_sub)"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.get("https://www.sonuker.com/login/final/" + req_dict['yt_channel_id'] + "/")  # Type_1
    driver.implicitly_wait(20)
    driver.save_screenshot("screenshots/screenshot.png")
    driver.save_screenshot("screenshots/screenshot.png")
    driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div > form >"
                                        " div:nth-child(2) > input").send_keys(req_dict['pw_sonuker'])

    driver.find_element_by_css_selector("#core-wrapper > section > div > div > div > div > div > form > button")\
        .send_keys(Keys.ENTER)
    driver.save_screenshot("screenshots/screenshot.png")
    driver.switch_to.default_content()
    try:
        if len(driver.find_elements_by_partial_link_text("Activated")) > 0:
            driver.quit()
            return
    except NoSuchElementException:
        logging.info("Couldn't find activate button ")
    driver.save_screenshot("screenshots/screenshot.png")
    try:
        driver.find_element_by_xpath("//*[@id='core-wrapper']/section/div/div/div[2]/div/div/div[2]/div[2]/" 
                                     "div[1]/div/div[2]/div[2]/form/a").click()
        time.sleep(2)
    except NoSuchElementException:
        logging.info("sonuker activate button passed 1")
        pass
    try:
        activate_btn = driver.find_element_by_css_selector("#core-wrapper > section > div > div > div:nth-child(2) >"
                                                           " div > div > div.userContent_pricing > div:nth-child(2) >"
                                                           " div:nth-child(1) > div > div.panel-body > div.btn-holder >"
                                                           " form > a")
        ActionChains(driver).move_to_element(activate_btn).perform()
        activate_btn.click()
    except NoSuchElementException:
        logging.info("sonuker activate button passed 2")
        pass
    driver.switch_to.default_content()
    driver.save_screenshot("screenshots/screenshot.png")
    type_1_for_loop_like_and_sub(driver,
                                 "sonuker",
                                 req_dict)
    driver.quit()


def subscribersvideo_functions(req_dict: dict):
    """subscriber.video login and activate Free All-In-One plan then call inner subscribe loop function(for_loop)"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.implicitly_wait(10)
    driver.get("https://www.subscribers.video/")  # Type_2
    driver.minimize_window()
    driver.set_window_size(1900, 1050)
    try:
        if len(driver.find_elements_by_partial_link_text("Service Temporarily Unavailable")) > 0:
            logging.info("subscribersvideo Website Temporarily Unavailable, closing driver")
            driver.quit()
            return
        else:
            pass
    except NoSuchElementException as ex:
        logging.info("subscribersvideo"+str(ex))
        driver.quit()
        return
    driver.find_element_by_xpath("//*[@id='main-nav']/ul/li[4]/button").click()
    driver.find_element_by_id("inputEmail").send_keys(req_dict['email_subscribersvideo'])
    driver.find_element_by_id("inputIdChannel").send_keys(req_dict['yt_channel_id'])
    driver.find_element_by_id("buttonSignIn").click()
    time.sleep(1.25)
    try:
        WebDriverWait(driver, 10).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

    except TimeoutException:
        pass
    if len(driver.find_elements_by_partial_link_text("Your channel doesn't have any public video.")) > 0:
        logging.info("subscribersvideo Your channel doesn't have any public video"
                     " Please try to reload this page one more time.")
        driver.quit()
        return
    else:
        pass
    if len(driver.find_elements_by_id("buttonPlan6")) > 0:
        try:
            driver.find_element_by_css_selector("#reviewDialog > div.greenHeader > div > a > i").click()
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
            pass
        try:
            driver.find_element_by_id("buttonPlan6").click()
        except (UnexpectedAlertPresentException, NoSuchElementException):
            logging.info("subscribersvideo Button Passed")
    time.sleep(3)
    try:
        driver.save_screenshot("screenshots/screenshot.png")
    except UnexpectedAlertPresentException:
        pass
    if len(driver.find_elements_by_partial_link_text("Please come later")) > 0:
        logging.info("subscribersvideo FOUND PLEASE COME LATER TEXT, EXITING")
        driver.quit()
        return

    else:
        pass

    time.sleep(1.25)
    if len(driver.find_elements_by_xpath("//*[@id='content']/div/div/div[2]/div[15]/div/div[3]/button")) > 0 \
            or len(driver.find_elements_by_xpath("//*[@id='content']/div/div/div[2]/div[12]/div/div[3]/button")) > 0:
        logging.info("subscribersvideo found gray button")
        driver.quit()
        return
    else:
        driver.switch_to.default_content()

    def for_loop():
        try:
            logging.info("subscribersvideo loop started")
            i = 0
            for _ in range(1, 10000000000):
                if len(driver.find_elements_by_xpath(
                        "//*[@id='content']/div/div/div[2]/div[15]/div/div[3]/button")) > 0:
                    break
                else:
                    window_before_4 = driver.window_handles[0]
                    driver.save_screenshot("screenshots/screenshot.png")
                    if len(driver.find_elements_by_xpath(
                            "//*[@id='content']/div/div/div[2]/div[15]/div/div[3]/button")) > 0:
                        driver.quit()
                        break
                    if len(driver.find_elements_by_partial_link_text("Please come later")) > 0:
                        driver.quit()
                        logging.info("subscribersvideo found Please come later text, closing")
                        break
                    try:
                        driver.find_element_by_id("btnWatchLikeAndSubscribe").send_keys(Keys.ENTER)
                    except NoSuchElementException:
                        logging.info("subscribersvideo couldn't find watch and subscribe button, closing")
                        driver.quit()
                        break
                    window_after_4 = driver.window_handles[1]
                    driver.switch_to.window(window_after_4)
                    driver.switch_to.default_content()
                    window_after_4 = driver.window_handles[1]
                    driver.switch_to.window(window_after_4)
                    if len(driver.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                            and len(driver.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                                  "ytd-toggle-button-renderer[1]")) > 0:
                        if i == 0:
                            google_login(driver, req_dict)
                            i += 1

                        if len(driver.find_elements_by_css_selector(
                                "#top-level-buttons >" " ytd-toggle-button-renderer."
                                "style-scope." "ytd-menu-renderer.force-icon-button"
                                ".style-default-active")) > 0:
                            pass
                        else:
                            time.sleep(2)
                            driver.execute_script("document.querySelector('#top-level-buttons >"
                                                  " ytd-toggle-button-renderer:nth-child(1)').click()")
                        time.sleep(2)
                        driver.execute_script("document.querySelector('#subscribe-button >"
                                              " ytd-subscribe-button-renderer').click()")
                        driver.save_screenshot("screenshots/screenshot_proof.png")
                    else:
                        driver.switch_to.window(window_before_4)
                        driver.switch_to.default_content()
                        time.sleep(1.25)
                        driver.find_element_by_id("btnSkip").click()
                        continue
                    driver.switch_to.window(window_before_4)
                    while len(driver.find_elements_by_class_name("button buttonGray")) > 0:
                        time.sleep(1.5)
                    el = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, "btnSubVerify")))
                    el.click()
                    logging.info("subscribersvideo done sub & like")

        except UnexpectedAlertPresentException:
            try:
                WebDriverWait(driver, 2).until(ec.alert_is_present())
                alert_4 = driver.switch_to.alert
                alert_4.accept()
                time.sleep(1.25)
                if len(driver.find_elements_by_xpath("//*[@id='buttonPlan6']")) > 0:
                    try:
                        driver.find_element_by_xpath("//*[@id='buttonPlan6']").click()
                    except Exception as ex_4:
                        logging.info("subscribersvideo Couldn't able to click buttonPlan6 Exception: " + str(ex_4))
                        driver.close()
                        return
                time.sleep(1.25)
                for_loop()
            except TimeoutException:
                logging.info("subscribersvideo outer timeout exception")
                for_loop()

    for_loop()
    driver.quit()


def submenow_functions(req_dict: dict):
    """submenow login and activate Jet All-In-One plan then call inner subscribe loop function(for_loop)"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.minimize_window()
    driver.set_window_size(1800, 900)
    driver.implicitly_wait(10)
    driver.get("https://www.submenow.com/")  # Type_2
    try:
        if len(driver.find_elements_by_partial_link_text("Service Temporarily Unavailable")) > 0:
            logging.info("submenow Website Temporarily Unavailable, closing driver")
            driver.quit()
            return
        else:
            pass
    except NoSuchElementException as ex:
        logging.info("submenow" + str(ex))
        driver.quit()
        return
    driver.find_element_by_xpath("//*[@id='header-wrapper']/div[2]/div[1]/div/button").click()
    driver.find_element_by_xpath("//*[@id='inputEmail']").send_keys(req_dict['email_submenow'])
    driver.find_element_by_xpath("//*[@id='inputIdChannel']").send_keys(req_dict['yt_channel_id'])
    driver.find_element_by_xpath("//*[@id='buttonSignIn']").click()
    time.sleep(1.25)
    if len(driver.find_elements_by_partial_link_text("Your channel doesn't have any public video.")) > 0:
        logging\
            .info("submenow Your channel doesn't have any public video Please try to reload this page one more time.")
        driver.quit()
        return
    else:
        pass
    if len(driver.find_elements_by_xpath("//*[@id='buttonPlan6']")) > 0:
        try:
            driver.find_element_by_css_selector("#reviewDialog > div.headerPlan > div > a > img").click()
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
            pass
        driver.find_element_by_xpath("//*[@id='buttonPlan8']").click()
    else:
        logging.info("submenow active Button Passed")
        driver.quit()
        return
    time.sleep(1.25)
    try:
        driver.save_screenshot("screenshots/screenshot.png")
    except UnexpectedAlertPresentException:
        pass
    if len(driver.find_elements_by_xpath("//*[@id='mainContentWrapper']/div[18]/div[3]/div[3]/button")) > 0:
        driver.quit()
        return
    if len(driver.find_elements_by_css_selector("#errorAjax > i")) > 0:
        logging.info("submenow found error dialog")
        driver.quit()
        return

    def for_loop():
        i = 0
        try:
            logging.info("submenow loop started")
            for _ in range(1, 1000000000):
                if len(driver.find_elements_by_xpath("//*[@id='mainContentWrapper']/div[18]/div[3]/div[3]/button")) > 0:
                    break
                else:
                    window_before_5 = driver.window_handles[0]
                    if len(driver.find_elements_by_id("buttonPlan1")) > 0 or len(driver.find_elements_by_xpath(
                            "//*[@id='content']/div/div/div[2]/div[15]/div/div[3]/button")) > 0:
                        break
                    try:
                        while driver.find_element_by_css_selector("#marketStatus > span").text != \
                                "Watch, Like & Subscribe":
                            time.sleep(1.25)
                    except StaleElementReferenceException:
                        logging.info("Couldn't find [Watch, Like & Subscribe] element closing")
                        driver.quit()
                    driver.save_screenshot("screenshots/screenshot.png")
                    driver.find_element_by_id("btnWatchLikeAndSubscribe").send_keys(Keys.ENTER)
                    window_after_5 = driver.window_handles[1]
                    driver.switch_to.window(window_after_5)
                    window_after_5 = driver.window_handles[1]
                    driver.switch_to.window(window_after_5)
                    driver.execute_script("window.scrollTo(0, 300)")
                    driver.save_screenshot("screenshots/screenshot.png")
                    if len(driver.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                            and len(driver.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                                  "ytd-toggle-button-renderer[1]")) > 0:
                        if i == 0:
                            google_login(driver, req_dict)
                            i += 1
                        if len(driver.find_elements_by_css_selector(
                                "#top-level-buttons > ytd-toggle-button-renderer."
                                "style-scope." "ytd-menu-renderer.force-icon-button"
                                ".style-default-active")) > 0:
                            pass
                        else:
                            time.sleep(2)
                            driver.execute_script("document.querySelector('#top-level-buttons >"
                                                  " ytd-toggle-button-renderer:nth-child(1)').click()")
                        time.sleep(2)
                        driver.execute_script("document.querySelector('#subscribe-button >"
                                              " ytd-subscribe-button-renderer').click()")
                        driver.save_screenshot("screenshots/screenshot_proof.png")

                    else:
                        driver.switch_to.window(window_before_5)
                        driver.find_element_by_id("btnSkip").send_keys(Keys.ENTER)
                        continue
                    driver.switch_to.window(window_before_5)
                    try:
                        driver.save_screenshot("screenshots/screenshot.png")
                        while len(driver.find_elements_by_class_name("button buttonGray")) > 0:
                            time.sleep(1.5)
                        driver.save_screenshot("screenshots/screenshot.png")
                        el = \
                            WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, "btnSubVerify")))
                        el.click()
                    except ElementNotInteractableException:
                        logging.info("submenow Found Element Not Interact able Exception, Quitting")
                        driver.quit()
                        return
                    logging.info("submenow done sub & like")
                    driver.save_screenshot("screenshots/screenshot.png")
                if len(driver.find_elements_by_xpath("//*[@id='dialog2']/div[3]/button")) > 0:
                    logging.info("submenow Found end dialog")
                    driver.quit()
                    return
        except UnexpectedAlertPresentException:
            try:
                WebDriverWait(driver, 2).until(ec.alert_is_present())
                alert_2 = driver.switch_to.alert
                alert_2.accept()
                if len(driver.find_elements_by_id("buttonPlan8")) > 0:
                    try:
                        driver.find_element_by_id("buttonPlan8").click()
                    except Exception as ex_5:
                        logging.info("submenow Alert Skipped Exception: " + str(ex_5))
                        driver.close()
                        return
                driver.find_element_by_id("btnReload").send_keys(Keys.ENTER)
                for_loop()

            except TimeoutException:
                for_loop()
    for_loop()
    driver.quit()


def ytmonster_functions(req_dict: dict):
    """ytmonster login and then earn credits by liking videos with inner like loop function(for_loop_sub)"""
    driver: webdriver = set_driver_opt(req_dict, True, "ytmonster")
    driver.implicitly_wait(15)
    driver.get("https://www.ytmonster.net/login")  # Type_None
    driver.find_element_by_id('inputUsername').send_keys(req_dict['username_ytmonster'])
    driver.find_element_by_id('inputPassword').send_keys(req_dict['pw_ytmonster'])
    driver.find_element_by_css_selector("#formLogin > button").send_keys(Keys.ENTER)
    driver.get("https://www.ytmonster.net/exchange/likes")
    driver.save_screenshot("screenshots/screenshot.png")

    def for_loop_sub(driver_6,
                     like_btn="likeText",
                     skip_btn="body > div.container-fluid > div > div.main > div.mainContent > div > div.col-md-9 >"
                              " div > div:nth-child(7) > div > a.likeSkip > div",
                     confirm_btn="body > div.container-fluid > div > div.main > div.mainContent > div > div.col-md-9 >"
                                 " div > div:nth-child(7) > div > div > div",
                     ):
        """ Loop for liking videos"""
        driver_6.save_screenshot("screenshots/screenshot.png")
        for i in range(50):
            window_before = driver_6.window_handles[0]
            driver_6.switch_to_window(window_before)
            driver_6.switch_to_default_content()
            time.sleep(2)
            driver_6.save_screenshot("screenshots/screenshot.png")
            while driver_6.find_element_by_css_selector("body > div.container-fluid > div > div.main >"
                                                        " div.mainContent >"
                                                        " div > div > div > div:nth-child(4) >"
                                                        " div.col-md-10.campaignData"
                                                        " > b") \
                    .text == "Loading...":
                continue
            time.sleep(1.25)
            driver_6.save_screenshot("screenshots/screenshot.png")
            yt_channel_name = driver_6.find_element_by_css_selector("""body > div.container-fluid > div > div.main > 
                                                                    div.mainContent > div > div > div >
                                                                    div:nth-child(4)
                                                                    > div.col-md-10.campaignData > b""") \
                .text
            if i == 0:
                i += 1
                time.sleep(1.25)
                try:
                    driver_6.save_screenshot("screenshots/screenshot.png")
                    driver_6.find_element_by_css_selector("#intercom-container > div > div > div > div >"
                                                          " div.intercom-tour-step-header > span").click()
                    logging.info("closed notification")
                except NoSuchElementException:
                    pass
                try:
                    driver_6.save_screenshot("screenshots/screenshot.png")
                    driver_6.find_element_by_id(like_btn).click()
                    logging.info("clicked like btn")
                except NoSuchElementException:
                    logging.info("Couldn't Find Like button")
                    driver_6.quit()
                    break
                window_after = driver_6.window_handles[1]
                driver_6.switch_to.window(window_after)
                google_login(driver_6, req_dict)
                driver_6.save_screenshot("screenshots/screenshot.png")
                logging.info("login completed")
                if len(driver.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                        and len(driver.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                              "ytd-toggle-button-renderer[1]")) > 0:
                    driver_6.save_screenshot("screenshots/screenshot.png")
                    driver_6.switch_to_default_content()
                    if len(driver_6.find_elements_by_css_selector("#top-level-buttons >"
                                                                  " ytd-toggle-button-renderer.style-scope."
                                                                  "ytd-menu-renderer.force-icon-button"
                                                                  ".style-default-active")) > 0:
                        pass
                    else:
                        time.sleep(2)
                        driver.execute_script("document.querySelector('#top-level-buttons >"
                                              " ytd-toggle-button-renderer:nth-child(1)').click()")
                    driver_6.save_screenshot("screenshots/screenshot_proof.png")
                    driver_6.switch_to.window(window_before)
                    driver_6.switch_to_default_content()
                    logging.info("Liked Channel")
                    for _ in range(50000):
                        if driver_6.find_element_by_css_selector("body > div.container-fluid > div > div.main >"
                                                                 " div.mainContent > div > div.col-md-9 > div >"
                                                                 " div:nth-child(7) > div > div > div")\
                                .text != "Verify Like":
                            time.sleep(1)
                        else:
                            logging.info("confirm button is clickable")
                            break
                    try:
                        time.sleep(2)
                        confirm_el = WebDriverWait(driver_6, 5)\
                            .until(ec.element_to_be_clickable((By.CSS_SELECTOR, confirm_btn)))
                        ActionChains(driver).move_to_element(confirm_el).click().perform()

                        logging.info("confirm button was clicked")
                        i += 1
                        driver_6.save_screenshot("screenshots/screenshot.png")
                        while yt_channel_name == driver_6.find_element_by_css_selector("body > div.container-fluid > "
                                                                                       "div > div.main >"
                                                                                       " div.mainContent > div > div >"
                                                                                       " div > div:nth-child(4) >"
                                                                                       " div.col-md-10.campaignData "
                                                                                       "> b")\
                                .text:
                            time.sleep(1.25)
                            if driver_6.find_element_by_id("error").text == \
                               "We failed to verify your like as we did not find an increase in the number" \
                               " of likes. Try verifying again, or skip the video.":

                                driver_6.find_element_by_css_selector(skip_btn).click()
                                logging.info("Skip button has been pressed")
                            continue
                        continue
                    except NoSuchElementException:
                        time.sleep(2)
                        window_after = driver_6.window_handles[1]
                        driver_6.switch_to.window(window_after)
                        driver_6.close()
                        driver_6.switch_to.window(window_before)
                        logging.info("couldn't find confirm button")
                        i += 1
                        continue

                else:
                    driver_6.switch_to.window(window_before)
                    driver_6.switch_to_default_content()
                    driver_6.find_element_by_css_selector(skip_btn).click()

                    i += 1
                    while yt_channel_name == driver_6.find_element_by_css_selector("body > div.container-fluid > div >"
                                                                                   " div.main > div.mainContent > div >"
                                                                                   " div > div > div:nth-child(4) >"
                                                                                   " div.col-md-10.campaignData > b") \
                            .text:
                        time.sleep(2)
                        if driver_6.find_element_by_id("error").text == \
                                "We failed to verify your like as we did not find an increase in the number of likes." \
                                " Try verifying again, or skip the video.":
                            driver_6.find_element_by_css_selector(skip_btn).click()
                            logging.info("Skip button has been pressed")
                        driver_6.save_screenshot("screenshots/screenshot.png")
                        continue
                    continue

            else:
                driver_6.switch_to_window(window_before)
                driver_6.switch_to_default_content()
                time.sleep(2)
                driver_6.save_screenshot("screenshots/screenshot.png")
                try:
                    WebDriverWait(driver_6, 20).until(ec.element_to_be_clickable((By.ID, like_btn)))
                    driver_6.find_element_by_id(like_btn).click()
                except NoSuchElementException:
                    break
                window_after = driver_6.window_handles[1]
                driver_6.switch_to.window(window_after)
                if len(driver.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                        and len(driver.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                              "ytd-toggle-button-renderer[1]")) > 0:
                    driver_6.save_screenshot("screenshots/screenshot.png")
                    driver_6.switch_to_default_content()
                    if len(driver_6.find_elements_by_css_selector("#top-level-buttons >"
                                                                  " ytd-toggle-button-renderer.style-scope."
                                                                  "ytd-menu-renderer.force-icon-button"
                                                                  ".style-default-active")) > 0:
                        pass
                    else:
                        time.sleep(2)
                        driver.execute_script("document.querySelector('#top-level-buttons >"
                                              " ytd-toggle-button-renderer:nth-child(1)').click()")
                    driver_6.save_screenshot("screenshots/screenshot_proof.png")
                    driver_6.switch_to.window(window_before)
                    driver_6.switch_to_default_content()
                    logging.info("Liked Channel")
                    driver_6.switch_to_default_content()
                    for _ in range(500000):
                        if driver_6.find_element_by_css_selector("body > div.container-fluid > div > div.main >"
                                                                 " div.mainContent > div > div.col-md-9 > div >"
                                                                 " div:nth-child(7) > div > div > div") \
                                .text != "Verify Like":
                            time.sleep(1.25)
                        else:
                            logging.info("confirm button is clickable")
                            break
                    try:
                        time.sleep(3)
                        driver_6.find_element_by_css_selector(confirm_btn).click()

                        logging.info("confirm button was clicked")
                        while yt_channel_name == driver_6.find_element_by_class_name("yt-name").text:
                            time.sleep(1.25)
                            if driver_6.find_element_by_id("error").text == \
                               "We failed to verify your like as we did not find an increase in the number of likes." \
                               " Try verifying again, or skip the video.":
                                driver_6.find_element_by_css_selector(skip_btn).click()
                                logging.info("Skip button has been pressed")
                    except NoSuchElementException:
                        time.sleep(3)
                        window_after = driver_6.window_handles[1]
                        driver_6.switch_to.window(window_after)
                        driver_6.close()
                        driver_6.switch_to.window(window_before)
                        logging.info("couldn't find confirm button")
                        continue

    for_loop_sub(driver)
    logging.info("Channels liked successfully, quitting driver")
    driver.quit()


def ytbpals_functions(req_dict: dict):
    """ytbpals login and then call inner subscribe loop function(for_loop_sub) finally activate free plan"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.implicitly_wait(10)
    driver.get("https://ytbpals.com/")  # Type_None
    driver.find_element_by_css_selector("#main_menu > ul > li:nth-child(6) > a").send_keys(Keys.ENTER)
    driver.find_element_by_id('email').send_keys(req_dict['email_ytbpals'])
    driver.find_element_by_id("password").send_keys(req_dict['pw_ytbpals'])
    driver.find_element_by_css_selector("#form_login > div:nth-child(3) > button").send_keys(Keys.ENTER)
    driver.find_element_by_css_selector("body > div.page-container.horizontal-menu > header > div > ul.navbar-nav >"
                                        " li:nth-child(5) > a").send_keys(Keys.ENTER)
    driver.save_screenshot("screenshots/screenshot.png")

    def for_loop_sub(driver_7, sub_btn="#ytbpals-channels > div > div > div >"
                                       " div.col-sm-4.text-center >"
                                       " button.subscribe.yt-btn.ytb-subscribe",
                     skip_btn="#ytbpals-channels > div > div > div > div.col-sm-4.text-center >"
                              " button.skip.yt-btn.ytb-subscribe.ytb-skip",
                     confirm_btn="ytbconfirm",
                     ):
        current_remaining_time = 0
        current_remaining = ""
        for i in range(0, 10000):
            logging.info("Loop Started")
            window_before = driver_7.window_handles[0]
            driver_7.switch_to_window(window_before)
            driver_7.switch_to_default_content()
            time.sleep(7)

            if i == 0:
                i += 1
                try:
                    driver_7.save_screenshot("screenshots/screenshot.png")
                    driver_7.find_element_by_css_selector(sub_btn).send_keys(Keys.ENTER)
                    logging.info("clicked Subscribe btn")
                except NoSuchElementException:
                    logging.info("No such Element Exception(sub_btn)")
                    driver_7.save_screenshot("screenshots/screenshot.png")
                    driver_7.find_element_by_css_selector("body > div.page-container.horizontal-menu > header > div >"
                                                          " ul.navbar-nav > li:nth-child(4) > a") \
                        .send_keys(Keys.ENTER)
                    try:
                        driver_7.find_element_by_css_selector("#inactive-plans > div.panel-body.with-table > table >"
                                                              " tbody > tr > td:nth-child(8) > button")\
                            .send_keys(Keys.ENTER)

                        driver_7.find_element_by_id("start-now")\
                            .send_keys(Keys.ENTER)
                        logging.info("Started plan successfully")

                    except Exception as ex:
                        logging.info("Error: Exception: " + str(ex))
                        driver_7.save_screenshot("screenshots/screenshot.png")
                    driver_7.quit()
                    break
                time.sleep(2)
                window_after = driver_7.window_handles[1]
                driver_7.switch_to.window(window_after)
                time.sleep(5)
                google_login(driver_7, req_dict)
                logging.info("login completed")
                if len(driver_7.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                        and len(driver_7.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                                "ytd-toggle-button-renderer[1]")) > 0:
                    driver_7.execute_script("window.scrollTo(0, 600);")
                    time.sleep(2)
                    driver_7.switch_to_default_content()
                    driver.execute_script("document.querySelector('#subscribe-button >"
                                          " ytd-subscribe-button-renderer').click()")
                    driver.save_screenshot("screenshots/screenshot_proof.png")
                    driver_7.close()
                    driver_7.switch_to.window(window_before)
                    driver_7.switch_to_default_content()
                    logging.info("Subbed to Channel")
                    driver_7.switch_to_default_content()
                    try:
                        time.sleep(2)
                        driver_7.find_element_by_id(confirm_btn).click()

                        logging.info("confirm button was clicked")
                        i += 1
                        continue
                    except NoSuchElementException:
                        time.sleep(2)
                        window_after = driver_7.window_handles[1]
                        driver_7.switch_to.window(window_after)
                        driver_7.close()
                        driver_7.switch_to.window(window_before)
                        logging.info("couldn't find confirm button")
                        i += 1
                        continue

                else:
                    driver_7.switch_to.window(window_before)
                    driver_7.switch_to_default_content()
                    driver_7.find_element_by_css_selector(skip_btn).send_keys(Keys.ENTER)

                    i += 1
                    continue

            else:
                driver_7.switch_to_window(window_before)
                driver_7.switch_to_default_content()
                time.sleep(7)
                try:
                    driver_7.find_element_by_css_selector(sub_btn).send_keys(Keys.ENTER)
                    logging.info("Remaining Videos:" + driver_7.find_element_by_id("ytbbal").text)
                    if driver_7.find_element_by_id("ytbbal").text == current_remaining:
                        current_remaining_time += 1
                        if current_remaining_time > 3:
                            logging.info("same remaining videos 4 times, resetting to begin function")
                            driver_7.quit()
                            ytbpals_functions(req_dict)
                            break
                    else:
                        current_remaining = driver_7.find_element_by_id("ytbbal").text
                        current_remaining_time = 0

                except NoSuchElementException:
                    logging.info("All channels were subscribed, activating free plan")
                    driver_7.save_screenshot("screenshots/screenshot.png")
                    driver_7.find_element_by_css_selector("body > div.page-container.horizontal-menu > header > div >"
                                                          " ul.navbar-nav > li:nth-child(4) > a")\
                        .send_keys(Keys.ENTER)
                    time.sleep(3)
                    driver_7.find_element_by_css_selector("#inactive-plans > div.panel-heading >"
                                                          " div.panel-options > a:nth-child(2)")\
                        .send_keys(Keys.ENTER)
                    time.sleep(2)
                    driver_7.find_element_by_css_selector("#inactive-plans > div.panel-heading >"
                                                          " div.panel-options > a:nth-child(2)") \
                        .send_keys(Keys.ENTER)
                    time.sleep(2)
                    try:
                        button = driver_7.find_element_by_css_selector("#inactive-plans > div.panel-body.with-table >"
                                                                       " table > tbody > tr > td:nth-child(8) > button")
                        button.send_keys(Keys.ENTER)
                        time.sleep(3)
                        button = driver_7.find_element_by_id("start-now")
                        ActionChains(driver_7).move_to_element(button).click(button).perform()

                        logging.info("Started plan successfully")
                    except Exception as ex:
                        logging.info("Error:" + str(ex))
                    driver_7.quit()
                    break
                time.sleep(3)
                window_after = driver_7.window_handles[1]
                driver_7.switch_to.window(window_after)
                if len(driver.find_elements_by_xpath("//*[@id='container']/h1/yt-formatted-string")) > 0 \
                        and len(driver.find_elements_by_xpath("//*[@id='top-level-buttons']/"
                                                              "ytd-toggle-button-renderer[1]")) > 0:
                    driver_7.execute_script("window.scrollTo(0, 600);")
                    time.sleep(2)
                    driver_7.save_screenshot("screenshots/screenshot.png")
                    driver_7.switch_to_default_content()
                    driver.execute_script("document.querySelector('#subscribe-button >"
                                          " ytd-subscribe-button-renderer').click()")
                    driver.save_screenshot("screenshots/screenshot_proof.png")
                    driver_7.close()
                    driver_7.switch_to.window(window_before)
                    driver_7.switch_to_default_content()
                    logging.info("Subbed to Channel")
                    driver_7.switch_to_default_content()
                    try:
                        time.sleep(2)
                        driver_7.find_element_by_id(confirm_btn).click()
                        logging.info("confirm button was clicked")
                        continue
                    except NoSuchElementException:
                        time.sleep(2)
                        window_after = driver_7.window_handles[1]
                        driver_7.switch_to.window(window_after)
                        driver_7.close()
                        driver_7.switch_to.window(window_before)
                        logging.info("couldn't find confirm button")
                        continue

    for_loop_sub(driver)


def goviral_functions(req_dict: dict):
    """goviral login and then earn credits by liking videos with inner like loop function(for_loop_sub)"""
    driver: webdriver = set_driver_opt(req_dict)
    driver.implicitly_wait(6)
    driver.get("https://accounts.google.com/signin/v2/identifier")
    google_login(driver, req_dict, has_sign_in_btn=False)
    logging.info("youtube login completed")
    time.sleep(3)
    driver.get("https://members.goviral.ai/")  # Type_None
    driver.find_element_by_name("email").send_keys(req_dict['email_goviral'])
    driver.find_element_by_name("password").send_keys(req_dict['pw_goviral'])
    driver.find_element_by_css_selector("#loginForm > div.kt-login__actions.justify-content-around >"
                                        " button").click()

    driver.find_element_by_css_selector("#kt_aside_menu > ul > li:nth-child(4) > a > span.kt-menu__link-text").click()
    driver.save_screenshot("screenshots/screenshot.png")

    def for_loop_like(driver_9,
                      like_btn_available="#kt_content > div > div.col-md-8 > div > form > div >"
                                         " div.disabled-area.position-relative >"
                                         " section.earn-likes.earning-box.position-relative.disabled",
                      subscribe_btn_available="#kt_content > div > div.col-md-8 > div > form > div >"
                                              " div.disabled-area.position-relative >"
                                              " section.earn-subscribes.earning-box.position-relative.disabled",
                      like_btn="#kt_content > div > div.col-md-8 > div > form > div >"
                               " div.disabled-area.position-relative >"
                               " section.earn-likes.earning-box.position-relative > div.row >"
                               " div.col-4.text-right.mt-1.position-relative > button",
                      subscribe_btn="#kt_content > div > div.col-md-8 > div > form > div >"
                                    " div.disabled-area.position-relative >"
                                    " section.earn-subscribes.earning-box.position-relative >"
                                    " div.row > div.col-4.text-right.mt-1.position-relative > button",
                      next_btn="#kt_content > div > div.col-md-8 > div > form > div > div.text-right.mt-3 >"
                               " button.btn.btn-primary.next-video.mr-3",
                      skip_btn="#kt_content > div > div.col-md-8 > div > form > div > div.text-right.mt-3 >"
                               " button.btn.btn-secondary.skip-video"
                      ):
        logging.info("Loop Started")
        for i in range(50):
            driver_9.save_screenshot("screenshots/screenshot.png")
            while len(driver_9.find_elements_by_class_name("time-remaining-amount")) == 0:
                time.sleep(1)
            x = 0
            while len(driver_9.window_handles) == 1:
                time.sleep(1)
                x += 1
                if x >= 30:
                    driver_9.refresh()
                    break
            if x >= 30:
                continue
            # print(x)
            driver_9.save_screenshot("screenshots/screenshot.png")
            try:
                driver_9.find_element_by_xpath("//*[@id='kt_content']/div/div[1]/div/form/div/div[1]/div/div/button")\
                    .send_keys(Keys.ENTER)
                logging.info("Enable button has been pressed")
                driver_9.refresh()
                time.sleep(3.25)
                continue
            except (NoSuchElementException,
                    ElementNotInteractableException,
                    TimeoutException,
                    StaleElementReferenceException):
                pass
            try:
                el = driver_9.find_element_by_css_selector("#kt_content > div > div.col-md-8 > div > form > div >"
                                                           " section > div > div.col-md-12 > div")
                if el.is_displayed() and len(driver_9.find_elements_by_css_selector(subscribe_btn_available)) == 0 and \
                        len(driver_9.find_elements_by_css_selector(like_btn_available)) == 0:
                    driver_9.find_element_by_css_selector(skip_btn).click()
                    time.sleep(3.25)
                    continue

            except (NoSuchElementException,
                    ElementNotInteractableException,
                    TimeoutException,
                    StaleElementReferenceException):
                pass
            try:
                while int(driver_9.find_element_by_class_name("time-remaining-amount").text) < 5:
                    time.sleep(0.75)
            except (StaleElementReferenceException, ValueError):
                driver_9.refresh()
                time.sleep(3)
                continue
            driver_9.save_screenshot("screenshots/screenshot.png")
            while int(driver_9.find_element_by_class_name("time-remaining-amount").text) > 17:
                time.sleep(0.75)
            if len(driver_9.find_elements_by_css_selector(subscribe_btn_available)) == 0:
                try:
                    driver_9.find_element_by_css_selector(subscribe_btn).click()
                    driver_9.switch_to.window(driver_9.window_handles[1])
                    try:
                        driver_9.execute_script("window.scrollTo(0, 300)")
                    except TimeoutException:
                        pass
                    time.sleep(3)
                    try:
                        driver_9.execute_script("document.querySelector('#subscribe-button >"
                                                " ytd-subscribe-button-renderer').click()")
                    except NoSuchWindowException:
                        pass
                    driver_9.switch_to.window(driver_9.window_handles[0])
                    driver_9.save_screenshot("screenshots/screenshot.png")
                    logging.info("Subscribed To Channel")
                except ElementClickInterceptedException:
                    pass
            if len(driver_9.find_elements_by_css_selector(like_btn_available)) == 0:
                try:
                    driver_9.save_screenshot("screenshots/screenshot.png")
                    driver_9.find_element_by_css_selector(like_btn).click()
                    driver_9.switch_to.window(driver_9.window_handles[1])
                    time.sleep(3)
                    if len(driver_9.find_elements_by_css_selector("#top-level-buttons >"
                                                                  " ytd-toggle-button-renderer.style-scope."
                                                                  "ytd-menu-renderer.force-icon-button"
                                                                  ".style-default-active")) > 0:
                        pass
                    else:
                        time.sleep(2)
                        # driver_9.save_screenshot("screenshots/screenshot.png")
                        try:
                            driver_9.execute_script("document.querySelector('#top-level-buttons >"
                                                    " ytd-toggle-button-renderer:nth-child(1)').click()")
                        except NoSuchWindowException:
                            pass
                    driver_9.switch_to.window(driver_9.window_handles[0])
                    logging.info("Liked Video")
                    driver_9.save_screenshot("screenshots/screenshot.png")
                except ElementClickInterceptedException:
                    pass
            try:
                while driver_9.find_element_by_class_name("time-remaining-amount").text != "0":
                    pass
            except StaleElementReferenceException:
                driver_9.refresh()
                time.sleep(3)
                continue
            c = 0
            while driver_9.find_element_by_class_name("time-remaining-amount").text == "0":
                time.sleep(0.5)
                c += 1
                if c >= 30:
                    try:
                        driver_9.find_element_by_css_selector(next_btn).send_keys(Keys.ENTER)
                    except (ElementNotInteractableException,
                            StaleElementReferenceException):
                        pass

    for_loop_like(driver)
    logging.info("Channels liked successfully, quitting driver")
    driver.quit()
