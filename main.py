from functions import *
from master_functions import *
import json


with open('test.json') as f:
    data = json.load(f)


code_list = []

for i in data:

    spaceSt = '' if i['parameters'] else ' '

    i = exceptional_operations(i)

    hierarcy_add = ("\t" * (i['hierarcy']))

    brSt = ['', ''] if i['d_parameter'] else ['(', ')']

    returnSt = str(i['return_variable'])+"=" if i['return_variable'] else ""

    cont = f"{hierarcy_add}{returnSt}{i['component_name']}{brSt[0]}{','.join([ str(k['parameter_name']) +'=' +str(k['parameter_value']) for k in i['parameters']])}{spaceSt}{i['d_parameter']}{brSt[1]}"

    code_list.append(cont)


run_code = "\n".join(code_list)

print(run_code)
