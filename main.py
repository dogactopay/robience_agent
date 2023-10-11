from functions import *
from master_functions import *
import time
from colorama import Fore, Back, Style


license_key = "lxeOM0OMxI"


response_config = get_data(f"/agent/{license_key}/config/")


if response_config.status_code == 200:

    time_interval = int(response_config.json()["config"]['fetch_timeout'])

    if response_config.json()['is_active']:

        while True:
            response = get_data(f"/agent/{license_key}/pending_job/").json()
            if response:

                data = response[0]['content']

                # with open('test.json') as f:
                #     data = json.load(f)

                run_code = generate_code(data)

                try:
                    exec(run_code)
                except Exception as e:
                    set_status(response[0]['job_id'], 2, str(e))
                else:
                    set_status(response[0]['job_id'], 1, "SUCCESS")
            else:
                print(Fore.YELLOW + "Waiting job.")
                time.sleep(time_interval)
    else:
        print(Fore.RED + "Agent is not active.Please contact with Robenice Support Team.")
else:
    print(Fore.RED + "License Key is not valid.")
