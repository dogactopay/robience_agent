import requests


def generate_code(data):
    code_list = []

    for i in data:

        spaceSt = '' if i['parameters'] else ' '

        i = exceptional_operations(i)

        hierarcy_add = ("\t" * (i['hierarcy']))

        brSt = ['', ''] if i['d_parameter'] else ['(', ')']

        returnSt = str(i['return_variable']) + \
            "=" if i['return_variable'] else ""

        cont = f"{hierarcy_add}{returnSt}{i['component_name']}{brSt[0]}{','.join([ str(k['parameter_name']) +'=' +str(k['parameter_value']) for k in i['parameters']])}{spaceSt}{i['d_parameter']}{brSt[1]}"

        code_list.append(cont)

    run_code = "\n".join(code_list)

    return run_code


def exceptional_operations(i):
    if "set_parameter" in i['component_name']:
        i['component_name'] = ""
        i['d_parameter'] = (str([k["parameter_value"] for k in i['parameters'] if k["parameter_name"] == 'variable_name'
                                 ][0]) + "=" + str([k["parameter_value"] for k in i['parameters'] if k["parameter_name"] == 'variable_value'
                                                    ][0]))
        i['parameters'] = []

    return i


def get_data(text):

    server = "http://localhost:8000"

    response = requests.get(
        f"{server}{text}")
    return response


def set_status(job_id, status,job_response):

    server = "http://localhost:8000"

    response = requests.patch(
        f"{server}/job/{job_id}/", data={"status": status, "job_response":job_response})
    return response
