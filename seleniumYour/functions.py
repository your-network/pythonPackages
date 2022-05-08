import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium_stealth import stealth
import platform
from time import sleep
import pickle

def start_driver(driver_status,driver_type):
    current_directory = os.getcwd()
    ## options
    options = Options()
    arguments = ["--disable-browser-side-navigation", f"user-data-dir={current_directory}/chrome_profiles/",
                 "--profile-directory=Profile 21", "start-maximized",
                 "--disable-blink-features=AutomationControlled", "--no-first-run --no-service-autorun --password-store=basic",
                 "--enable-javascript", "--disable-gpu",
                 "--disable-dev-shm-usage", "--no-sandbox"]
    for argument in arguments:
        options.add_argument(argument)
    ## special cases
    options.add_argument('useAutomationExtension', False)
    options.add_argument("excludeSwitches", ["enable-automation"])
    ## saved arguments
    #     options.add_argument("--headless")
    #     options.add_argument("--log-level=3")
    #     options.add_argument("--proxy-server=us-wa.proxymesh.com:31280")
    if driver_status == 'start':
        if driver_type == 'FIREFOX':
            os_platform = platform.platform()
            if 'macOS' in os_platform:
                driver_path = f"{current_directory}/geckodriver"
            else:
                driver_path = f"{current_directory}/geckodriver.exe"
            driver = webdriver.Firefox(executable_path=driver_path)
        elif driver_type == 'CHROME':
            os_platform = platform.platform()
            if 'macOS' in os_platform:
                driver_path = f"{current_directory}/chromedriver"
            else:
                driver_path = f"{current_directory}/chromedriver.exe"
            driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
    else:
        print('driver start fail')
    return driver

def scroll_page(driver, start, end, direction):
    if direction == 'down':
        traps = (end - start) / 4
        driver.execute_script(f"window.scrollTo({start}, {traps})")
        sleep(1)
        driver.execute_script(f"window.scrollTo({traps}, {traps * 2})")
        sleep(2)
        driver.execute_script(f"window.scrollTo({traps * 2}, {traps * 3})")
        sleep(1)
        driver.execute_script(f"window.scrollTo({traps * 3}, {traps * 4})")
    elif direction == 'up':
        traps = (end - start) / 4 * -1
        traps_1 = start - traps
        driver.execute_script(f"window.scrollTo({start}, {start - traps})")
        sleep(1)
        driver.execute_script(f"window.scrollTo({start - traps}, {start - traps * 2})")
        sleep(2)
        driver.execute_script(f"window.scrollTo({start - traps * 2}, {start - traps * 3})")
        sleep(1)
        driver.execute_script(f"window.scrollTo({start - traps * 3}, {start - traps * 4})")
    return print(f"Scroll {direction} from {start} to {end}")

def move_mouse_directions(driver, element):
    action = ActionChains(driver)
    action.move_to_element(element)
    action.move_by_offset(8, 1)
    action.move_by_offset(6, 1)
    action.move_by_offset(4, 1)
    action.move_by_offset(2, 1)
    action.move_by_offset(1, 1)
    action.move_by_offset(1, 2)
    action.move_by_offset(1, 4)
    action.move_by_offset(1, 6)
    action.move_by_offset(1, 8)
    action.release()
    action.perform()
    return print(f"Human mouse moved")


def store_cookies(cookies):
    try:
        old_cookies = cookies = pickle.load(open("cookies.pkl", "rb"))
        print(f"Old cookies: {len(old_cookies)}")
        new_cookies = old_cookies + cookies
        print(f"New cookies: {len(new_cookies)}")
        pickle.dump(new_cookies, open("cookies.pkl", "wb"))
    except:
        pickle.dump(cookies, open("cookies.pkl", "wb"))


def set_stored_cookies(driver):
    if os.path.isfile("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        cookies_set = 0
        for count, cookie in enumerate(cookies):
            try:
                driver.add_cookie(cookie)
                cookies_set += 1
            except exceptions.InvalidCookieDomainException as e:
                print(e)
                pass
        print(f"Cookies added. Number: {cookies_set}")
