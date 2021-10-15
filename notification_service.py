import smtplib, ssl
import json
import yagmail
import os

port = 465
EMAIL = ""
PASSWORD = ""
CONFIG_DIR = './configs'

with open("notification_info.json") as f:
    info = json.load(f)
    EMAIL = info["email"]
    PASSWORD = info["password"]

def create_message()->str:
    # # TODO: Loop through configs and create structured text
    # Set cronjob on server
    friday_str = "Reservations this Friday:\r\r"
    saturday_str = "Reservations this Saturday:\r\r"
    # Loop through the configs
    for filename in os.listdir(CONFIG_DIR):
        with open(os.path.join(CONFIG_DIR, filename)) as f:
            config = json.load(f)

            if config['reservations']['this_friday']:
                friday_str = friday_str + f"{config['name']} - {config['times']['this_friday']} - {config['form_info']['account']} \r"

            if config['reservations']['this_saturday']:
                saturday_str = saturday_str + f"{config['name']} - {config['times']['this_saturday']} - {config['form_info']['account']} \r"

    return f"{friday_str}\r{saturday_str}"


def main():
    yag = yagmail.SMTP(EMAIL, PASSWORD)

    notification = create_message()
    #Tony
    yag.send(to="8605957517@tmomail.net", contents=notification)
    #Will
    yag.send(to="3392255981@vtext.com", contents=notification)
    #RJ
    yag.send(to="6175152748@txt.att.net", contents=notification)
    #Paul
    yag.send(to="5086426730@tmomail.net", contents=notification)




if __name__ == "__main__":
    main()
