from Reserve import Reservation
import logging, coloredlogs, verboselogs
import pendulum
from selenium import webdriver
import json
import os
from pyvirtualdisplay import Display

CONFIG_DIR= './configs'
ACCOUNTS_FILE = open('accounts.json')
ACCOUNTS = json.load(ACCOUNTS_FILE)
log = verboselogs.VerboseLogger('reservation_service')

def main():

    configs = []
    # Load all of our restaurant configs into a list
    for filename in os.listdir(CONFIG_DIR):
        with open(os.path.join(CONFIG_DIR, filename)) as f:
            config = json.load(f)
            configs.append(config)
            f.close()


    # Browser initialization
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    for restaurant in configs:
        log.success(f"STARTING RUN FOR {restaurant['name']} !")
        browser = webdriver.Firefox()
        try:
            Reservation(browser, restaurant, ACCOUNTS[restaurant['form_info']['account']]).reserve()
        except Exception as e:
            log.error(f"Error reserving for {restaurant['name']}: {e}")
        browser.quit()

    display.stop()



if __name__ == "__main__":
    main()
