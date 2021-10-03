import json
import pendulum
import os
import logging

logging.basicConfig(filename="rotationlog.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
log = logging.getLogger("rotation_service.py")

def main():
    log.info(f"Starting rotation service on {pendulum.now()}")
    try:
        config_dir = './configs'
        today = pendulum.now().day_of_week
        config = {}

        if today == 5:
            for filename in os.listdir(config_dir):
                with open(os.path.join(config_dir, filename)) as f:
                    config = json.load(f)

                    log.info(f"Moving reservations next Friday to this Friday: {filename}")
                    config["reservations"]["this_friday"] = config["reservations"]["next_friday"]
                    config["reservations"]["next_friday"] = False

                    f.close()

                with open(os.path.join(config_dir, filename), "w") as f:
                    json.dump(config, f, indent=2)
                    f.close()
        if today == 6:
            for filename in os.listdir(config_dir):
                with open(os.path.join(config_dir, filename)) as f:
                    config = json.load(f)

                    log.info(f"Moving reservations next Saturday to this Saturday: {filename}")
                    config["reservations"]["this_saturday"] = config["reservations"]["next_saturday"]
                    config["reservations"]["next_saturday"] = False

                    f.close()

                with open(os.path.join(config_dir, filename), "w") as f:
                    json.dump(config, f, indent=2)
                    f.close()
    except Exception as e:
        log.error(f"ERROR rotating reservation dates for {config} {e}")

if __name__ == "__main__":
    main()
