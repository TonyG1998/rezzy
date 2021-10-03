import smtplib, ssl
import json
import yagmail

port = 465
EMAIL = ""
PASSWORD = ""
CONFIG_DIR = './configs'

with open("notification_info.json") as f:
    json = json.load(f)
    EMAIL = json["email"]
    PASSWORD = json["password"]

def create_message()->str:
    # # TODO: Loop through configs and create structured text
    # Set cronjob on server
    friday_str =
    # Loop through the configs
    for filename in os.listdir(CONFIG_DIR):
        with open(os.path.join(CONFIG_DIR, filename)) as f:
            config = json.load(f)

def main():
    yag = yagmail.SMTP("530reservations@gmail.com", PASSWORD)

    notification = create_message()
    yag.send(to="8605957517@tmomail.net", contents=notification)



if __name__ == "__main__":
    main()
