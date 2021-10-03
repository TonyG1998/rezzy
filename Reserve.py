from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging, coloredlogs, verboselogs
import pendulum
import json


logging.basicConfig(filename="rezzylog.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
log = logging.getLogger("Reserve.py")

class Reservation:

    def __init__(self, browser, config, account):
        self.browser = browser
        self.config = config
        self.account = account

    @staticmethod
    def find_next_day(next_day, out=False):
        '''Finds the next day asked from the current date, and outputs in the format as opentable'''

        if out:
            if next_day == 'Friday':
                next_day = pendulum.now().next(pendulum.FRIDAY).next(pendulum.FRIDAY).format('ddd[,] MMM D[,] YYYY')

            if next_day == 'Saturday':
                next_day = pendulum.now().next(pendulum.SATURDAY).next(pendulum.SATURDAY).format('ddd[,] MMM D[,] YYYY')
        else:
            if next_day == 'Friday':
                next_day = pendulum.now().next(pendulum.FRIDAY).format('ddd[,] MMM D[,] YYYY')

            if next_day == 'Saturday':
                next_day = pendulum.now().next(pendulum.SATURDAY).format('ddd[,] MMM D[,] YYYY')

        return next_day

    def select_date(self, date_element, next_day, out=False):
        date_element.click()
        time.sleep(2)
        date = self.find_next_day(next_day, out)
        log.info(f"Clicking for next {next_day}... {date}")
        self.browser.find_element_by_xpath(f".//div[@aria-label='{date}']").click()
        time.sleep(2)

    def select_time(self, time_element, slot):
        time_element.click()
        time.sleep(4)
        log.info(f"Clicking time: {slot} ...")
        self.browser.find_element_by_xpath(f".//select[@data-auto='timeSlotsSelectMenu']/option[text()='{slot}']").click()
        time.sleep(2)

    def scan_tables(self, table_button):
        log.info("Finding tables...")
        table_button.click()
        time.sleep(5)

        time_slots = self.browser.find_elements_by_xpath(".//div[@data-auto='timeslot']")
        iterator = map(lambda slot: slot.text, time_slots)
        time_slots = list(iterator)

        return time_slots

    def select_party(self, party_element, party_size):
        party_element.click()
        time.sleep(2)
        log.info(f"Clicking party size {party_size}...")
        self.browser.find_element_by_xpath(f".//select[@data-auto='partySizeSelectMenu']/option[@value='{party_size}']").click()
        time.sleep(2)

    def find_tables(self, next_day, out=False):
        '''Returns a list of table slots. Takes the day of the week you are searching for and
        searches the next instance of that day'''
        self.browser.get(self.config['url'])

        party_element = self.browser.find_element_by_xpath(".//select[@data-auto='partySizeSelectMenu']")
        date_element = self.browser.find_element_by_xpath(".//button[@data-auto='expandCalendar']")
        time_element = self.browser.find_element_by_xpath(".//select[@data-auto='timeSlotsSelectMenu']")
        find_table_element = self.browser.find_element_by_xpath(".//button[@data-auto='findATableButton']")

        #Click on the party of 5 option
        self.select_party(party_element, '5')

        #Select 'next_day'
        self.select_date(date_element, next_day, out)

        #Click on the 8:30PM option
        self.select_time(time_element, '8:30 PM')

        time_slots = self.scan_tables(find_table_element)
        return time_slots

    def get_reservation(self, slot):
        date = self.browser.find_element_by_xpath(".//button[@data-auto='expandCalendar']/div").text
        slot_element = self.browser.find_element_by_xpath(f".//div[@data-auto='timeslot']/span[text()='{slot}']")
        log.info(f"Getting reservation for {date} at {slot}... ")
        slot_element.click()
        time.sleep(5)
        self.fill_form()

    def fill_form(self):
        log.info("Filling out reservation form...")
        log.info("Signing in")
        time.sleep(2)
        self.browser.find_element_by_xpath(".//button[@data-test='login-diner-button']").click()
        time.sleep(3)
        self.browser.switch_to.frame(self.browser.find_element_by_xpath(".//iframe[@title='Sign in']"))

        email_element = self.browser.find_element_by_xpath(".//input[@id='Email']")
        password_element = self.browser.find_element_by_xpath(".//input[@id='Password']")

        email_element.send_keys(self.account['email'])
        password_element.send_keys(self.account['password'])
        time.sleep(1)
        password_element.submit()
        log.info("Submitting info")
        time.sleep(5)

        self.browser.switch_to.default_content()
        time.sleep(2)

        #Wait for reservation to be clickable
        log.info("Waiting for reservation button to be clickable")
        wait = WebDriverWait(self.browser, 30)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[@id='complete-reservation']")))

        log.info("Filling phone number")
        phone_element = self.browser.find_element_by_xpath(".//input[@id='phoneNumber']")
        phone_element.clear()
        phone_element.send_keys(self.config['form_info']['phone_number'])
        time.sleep(2)

        log.info("Clicking reservation button")
        #TODO click reservation
        self.browser.find_element_by_xpath(".//button[@id='complete-reservation']").click()
        time.sleep(10)

    def update_config(self, day: str):
        self.config['reservations'][day] = True

        # TODO updates the restaurant config if a reservation is found for the given day.
        file_name = self.config['name']
        with open(f"configs/{file_name}.json", "w") as f:
            json.dump(self.config, f, indent=2)
            f.close()


    def reserve(self):
        ''' Check which days we already have reservations for. We only search on dates where we don't have a
        reservation for that restaurant'''

        if not self.config['reservations']['this_friday']:
            log.info("Searching for tables this Friday")
            time_slots = self.find_tables('Friday')

            if len(time_slots) != 0:
                # TODO function to decide what time to reserve
                log.info("Times found for this Friday!")
                log.info(f"Times: {time_slots}")
                try:
                    self.get_reservation(time_slots[-1])
                    self.update_config('this_friday')
                except Exception as e:
                    log.error(f"Error securing reservation: {e}")
            else:
                log.info("No tables found for this Friday")

        if not self.config['reservations']['this_saturday']:
            log.info("Searching for tables this Saturday")
            time_slots = self.find_tables('Saturday')

            if len(time_slots) != 0:
                # TODO function to decide what time to reserve
                log.info("Times found for this Saturday!")
                log.info(f"Times: {time_slots}")
                try:
                    self.get_reservation(time_slots[-1])
                    self.update_config('this_saturday')
                except Exception as e:
                    log.error(f"Error securing reservation: {e}")
            else:
                log.info("No tables found for this Saturday")

        if not self.config['reservations']['next_friday']:
            log.info("Searching for tables next Friday")
            time_slots = self.find_tables('Friday', out=True)

            if len(time_slots) != 0:
                # TODO function to decide what time to reserve
                log.info("Times found for next Friday!")
                log.info(f"Times: {time_slots}")
                try:
                    self.get_reservation(time_slots[-1])
                    self.update_config('next_friday')
                except Exception as e:
                    log.error(f"Error securing reservation: {e}")
            else:
                log.info("No tables found for next Friday")

        if not self.config['reservations']['next_saturday']:
            log.info("Searching for tables next Saturday")
            time_slots = self.find_tables('Saturday', out=True)

            if len(time_slots) != 0:
                # TODO function to decide what time to reserve
                log.info("Times found for next Saturday!")
                log.info(f"Times: {time_slots}")
                try:
                    self.get_reservation(time_slots[-1])
                    self.update_config('next_saturday')
                except Exception as e:
                    log.error(f"Error securing reservation: {e}")
            else:
                log.info("No tables found for next Saturday")
def main():
    test_config = open("./configs/broadway.json")
    config = json.load(test_config)
    ACCOUNTS = json.load(open("accounts.json"))

    browser = webdriver.Firefox()
    try:
        Reservation(browser, config, ACCOUNTS[config['form_info']['account']]).reserve()
    except Exception as e:
        log.error(f"Error reserving for {restaurant['name']}: {e}")
    browser.quit()

if __name__ == "__main__":
    main()
