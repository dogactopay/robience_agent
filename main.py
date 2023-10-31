from functions import *
from master_functions import *
import time
from colorama import Fore, Back, Style
import json

# LICANCE KEY FOR IDENTIFICATION


license_key = check_license_key()


# GET CONFIG VALUE FOR FETCH TIME INTERVAL AND IS_ACTIVE STATUS
response_config = get_data(f"/agent/{license_key}/config/")


if response_config.status_code == 200:

    time_interval = int(response_config.json()["config"]['fetch_timeout'])

    if response_config.json()['is_active']:

        while True:
            response = get_data(f"/agent/{license_key}/pending_job/").json()
            # with open('test.json') as f:
            #     response = json.load(f)

            if response:

                data = sort_code(response)

                run_code = generate_code(data)

                extra_parameters = create_extra_variables(response)
                embed()
                try:
                    # embed()
                    exec(run_code, None, extra_parameters)

                    print(run_code)

                except Exception as e:
                    print(e)
                    set_status(response[0]['job_id'], 0, str(e))

                else:
                    set_status(response[0]['job_id'], 0, "SUCCESS")

            print(Fore.YELLOW + "Waiting job.")
            time.sleep(time_interval)
            break

    else:
        print(Fore.RED + "Agent is not active.Please contact with Robenice Support Team.")
else:
    print(Fore.RED + "License Key is not valid.")
