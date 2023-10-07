from functions import *
###### TODO ######
# SET PARAMETER EKLENECEK
# GET PARAMETER EKLENECEK
# DATA İÇERİSİNDEKİ PARAMETRELER TEK TİP YAPILACAK
# D_PARAMETER KOŞULSUZ OLACAK
###### TODO ######


data = [
    {"component_name": "while",  "hierarcy": 0,
        "parameters": [], "d_parameter": "True:"},
    {"component_name": "if",  "hierarcy": 1,
        "parameters": [], "d_parameter": "a > 10:"},
    {"component_name": "yaz1", "hierarcy": 2,
        "parameters": [{"text": "'deneme'"}]},
]


code_list = []

for i in data:

    loop_add = ("\t" * (i['hierarcy']))

    if len(i["parameters"]) > 0:
        code_list.append(
            f"{loop_add}{i['component_name']}({','.join([f'{list(k.keys())[0]}={list(k.values())[0]}' for k in i['parameters']])})")

    elif "d_parameter" in list(i.keys()):
        code_list.append(
            f"{loop_add}{i['component_name']}{','.join([f'{list(k.keys())[0]}={list(k.values())[0]}' for k in i['parameters']])} {i['d_parameter']}")


run_code = "\n".join(code_list)

print(run_code)
