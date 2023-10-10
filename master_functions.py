def exceptional_operations(i):
    if "set_parameter" in i['component_name']:
        i['component_name'] = ""
        i['d_parameter'] = (str([k["parameter_value"] for k in i['parameters'] if k["parameter_name"] == 'variable_name'
                                 ][0]) + "=" + str([k["parameter_value"] for k in i['parameters'] if k["parameter_name"] == 'variable_value'
                                                    ][0]))
        i['parameters'] = []


    return i
