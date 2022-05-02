import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import platform
from time import sleep

def start_driver(driver_status,driver_type):
    current_directory = os.getcwd()
    ## options
    options = Options()
    #     options.add_argument("--headless")
    options.add_argument("user-data-dir=/Users/thijmenfrancken/repos/your/scrapers/chrome_profiles/")
    options.add_argument('--profile-directory=Profile 21')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('start-maximized')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.add_argument("--enable-javascript")
    #     options.add_argument("--log-level=3")
    #     options.add_argument("--proxy-server=us-wa.proxymesh.com:31280")
    options.add_argument('start-maximized')
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