import argparse, copy, ast

def newSubparser():
    return argparse.ArgumentParser(add_help = False, formatter_class = argparse.RawTextHelpFormatter)

def mySub(dict_class, dict_yaml, dict_default):
    mydict = copy.deepcopy(dict_class)
    for key in sorted(mydict):
        if mydict[key] is None:
            try:
                mydict[key] = dict_yaml[key]
            except KeyError:
                continue
        else:
            continue

    for attr in sorted(dict_default):
        if mydict[attr] is None:
            try:
                mydict[attr] = dict_default[attr]
            except KeyError:
                continue
        else:
            continue

    return mydict

def addCmd(instance_tool, name_tool, str_dict_add):
    dict_add = ast.literal_eval(str_dict_add)
    try:
        dict_add_sub = dict_add[name_tool]
    except KeyError:
        return instance_tool
    instance_tool + dict_add_sub
