import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import platform
from time import sleep

def get_driver_settings(driver_type):
    DRIVER_SETTINGS = {}
    DRIVER_SETTINGS['DRIVER'] = driver_type
    current_directory = os.getcwd()
    if driver_type == 'CHROME':
        if "macOS" in platform.platform():
            current_directory = current_directory.replace('/scraper', '')
            DRIVER_SETTINGS['DRIVER_PATH'] = "/Users/thijmenfrancken/Documents/python/pandas/chromedriver"
        else:
            DRIVER_SETTINGS['DRIVER_PATH'] = "/Users/thijmenfrancken/Documents/python/pandas/chromedriver"
    elif driver_type == 'FIREFOX':
        DRIVER_SETTINGS['DRIVER_PATH'] = "/Users/thijmenfrancken/Downloads/geckodriver"
    print(f"driver path: {DRIVER_SETTINGS['DRIVER_PATH']}")
    return DRIVER_SETTINGS

def start_driver(driver_status,driver_type,driver_path):
    ## options
    options = Options()
#     options.add_argument("--headless")
    options.add_argument("window-size=1400,600")
    if driver_status == 'start':
        driver_settings = get_driver_settings(driver_type)
        if driver_settings['DRIVER'] == 'FIREFOX':
            driver = webdriver.Firefox(executable_path=r'{driver_path}'.format(driver_path=driver_settings['DRIVER_PATH']))
        elif driver_settings['DRIVER'] == 'CHROME':
            driver = webdriver.Chrome(chrome_options=options, executable_path=r'{driver_path}'.format(driver_path=driver_settings['DRIVER_PATH']))
    elif driver_status == 'restart':
        driver.close()
        driver_settings = get_driver_settings(driver_type)
        if driver_settings['DRIVER'] == 'FIREFOX':
            driver = webdriver.Firefox(executable_path=r'{driver_path}'.format(driver_path=driver_settings['DRIVER_PATH']))
        elif driver_settings['DRIVER'] == 'CHROME':
            driver = webdriver.Chrome(executable_path=r'{driver_path}'.format(driver_path=driver_settings['DRIVER_PATH']))
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