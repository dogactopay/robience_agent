import requests
from IPython import embed
import time
import os


def root_folder_get():
    if os.name == 'nt':  # Windows
        file_path = os.path.join(os.path.expanduser(
            '~'), 'Documents/robenice_agent/')
    else:
        file_path = os.path.expanduser('~/Documents/robenice_agent/')
    return file_path


def check_license_key():
    while True:
        if os.name == 'nt':  # Windows
            file_path = os.path.join(os.path.expanduser(
                '~'), 'Documents/robenice_agent/key.txt')
        else:
            file_path = os.path.expanduser(
                '~/Documents/robenice_agent/key.txt')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                key1 = f.read()

                break

        else:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            key = input("Enter Licance Key : ")

            response_config = get_data(f"/agent/{key}/config/")

            if response_config.status_code == 200:
                with open(file_path, 'w') as f:
                    f.write(key)
            else:
                print("Not valid key!")
                time.sleep(5)
    return key1


def create_extra_variables(data):

    q = {f"ext_{k}": data[0]['extra_parameters'][k]
         for k in data[0]['extra_parameters']}
    q["ext_customer"] = data[0]['customer']

    return q


def set_hierarcy(data):

    for j, i in enumerate(data):

        if i['data']['component_type'] == 'builtinNode':

            if i['data']['component_name'] == "else":
                for z, t in enumerate(data[j:]):
                    t['data']['data']['hierarcy'] -= 1

            for z, t in enumerate(data[j+1:]):
                t['data']['data']['hierarcy'] += 1

        if i['data']['component_type'] == 'breakNode':

            for z, t in enumerate(data[j+1:]):
                t['data']['data']['hierarcy'] -= 1

    return data


def sort_code(response):

    edges = response[0]['scenario']['content']['edges']
    nodes = response[0]['scenario']['content']['nodes']

    initial = list(set([z['id'] for z in response[0]['scenario']['content']['nodes']]) -
                   set([z['target'] for z in response[0]['scenario']['content']['edges']]))[0]

    vp = [initial]
    zt = [z for z in nodes if z['id'] == initial]

    for t in vp:
        for k in edges:
            if k['source'] == t:
                vp.append(k['target'])
                zt.append([z for z in nodes if z['id'] == k['target']][0])

    response[0]['scenario']['content']['nodes'] = zt
    return response


def generate_code(data):

    code_list = []

    #extra_vars = create_extra_variables(data)

    data = data[0]['scenario']['content']['nodes']
    data = set_hierarcy(data)

    for i in data:
        if "parameters" not in i['data']['data'].keys():
            i['data']['data']['parameters'] = []

        spaceSt = '' if i['data']['data']['parameters'] else ' '

        i = exceptional_operations(i)

        hierarcy_add = ("\t" * (i['data']['data']['hierarcy']))

        brSt = ['', ''] if i['data']['data']['d_parameter'] or i['data']['component_type'] == 'breakNode' else [
            '(', ')']

        returnSt = str(i['data']['data']['return_variable']) + \
            "=" if i['data']['data']['return_variable'] else ""

        d_parameters = i['data']['data']['d_parameter'].replace(
            "{", "").replace(
            "}", "") if i['data']['data']['d_parameter'] else i['data']['data']['d_parameter'].replace(
            "{", "").replace(
            "}", "")

        contq = ','.join([str(k['parameter_name']) + '=' + (k['parameter_value'].replace("{", "").replace("}", "")
                                                            if k['parameter_value'][0] == "{" and k['parameter_value'][-1] == "}" and k['parameter_value'].count("{") < 2 else "f"+("'{}'".format(str(
                                                                k['parameter_value']).replace("'", '"'))))for k in i['data']['data']['parameters']])

        cont = f'''{hierarcy_add}{returnSt}{i['data']['component_name']}{brSt[0]}{contq}{spaceSt}{d_parameters}{brSt[1]}'''

        code_list.append(cont)

    run_code = "\n".join(code_list)

    return run_code


def exceptional_operations(i):

    if "set_variable" == i['data']['component_name']:
        i['data']['component_name'] = ""
        i['data']['data']['d_parameter'] = (str([k["parameter_value"] for k in i['data']['data']['parameters'] if k["parameter_name"] == 'variable_name'
                                                 ][0]) + "=" + str([k["parameter_value"] for k in i['data']['data']['parameters'] if k["parameter_name"] == 'variable_value'
                                                                    ][0]))

        i['data']['data']['parameters'] = []

    if "python_script" == i['data']['component_name']:

        i['data']['component_name'] = ""
        i['data']['data']['d_parameter'] = str([k["parameter_value"] for k in i['data']['data']['parameters'] if k["parameter_name"] == 'script'
                                                ][0])
        hierarcy_add = ("\t" * (i['data']['data']['hierarcy']))
        i['data']['data']['parameters'] = []

        i['data']['data']['d_parameter'] = i['data']['data']['d_parameter'].replace(
            "\n\n", "\n").replace("\n", f"\n{hierarcy_add}")


###### BUILT IN ELSE AYARI VE : AYARI ######
    if i['data']['component_type'] == "builtinNode":
        if ":" not in i['data']['data']['d_parameter']:
            i['data']['data']['d_parameter'] = i['data']['data']['d_parameter']+":"

        if i['data']['component_name'] == "else" and len(i['data']['data']['d_parameter']) > 2:
            i['data']['component_name'] = "elif"

    return i


def get_data(text):
    while True:
        try:

            server = "http://185.185.82.233/"

            response = requests.get(
                f"{server}{text}")
            return response
        except:
            print("Connection problem!")
            time.sleep(20)
        else:
            break


def set_status(job_id, status, job_response):
    server = "http://185.185.82.233/"

    response = requests.patch(
        f"{server}/job/{job_id}/", data={"status": status, "job_response": job_response}).json()
    return response
