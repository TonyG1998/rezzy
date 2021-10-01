import json
import pendulum
import os

def main():
    config_dir = './configs'
    today = pendulum.now().day_of_week
    config = {}

    if today == 5:
        for filename in os.listdir(config_dir):
            with open(os.path.join(config_dir, filename)) as f:
                config = json.load(f)

                config['reservations']['this_friday'] = config['reservations']['next_friday']
                config['reservations']['next_friday'] = False

                f.close()

            with open(os.path.join(config_dir, filename), "w") as f:
                json.dump(config, f, indent=2)
                f.close()
git
    if True:
        for filename in os.listdir(config_dir):
            with open(os.path.join(config_dir, filename)) as f:
                config = json.load(f)

                config['reservations']['this_saturday'] = config['reservations']['next_saturday']
                config['reservations']['next_saturday'] = False

                f.close()

            with open(os.path.join(config_dir, filename), "w") as f:
                json.dump(config, f, indent=2)
                f.close()

if __name__ == "__main__":
    main()
