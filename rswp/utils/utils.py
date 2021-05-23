import argparse, copy, ast, sys, colorama, time

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

def myNotification():
    sys.stdout.write(colorama.Fore.GREEN + "\n\n[NOTIFICATION {}] ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def myError():
    sys.stderr.write(colorama.Fore.RED + "\n\n[ERROR {}] ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def myWarning():
    sys.stdout.write(colorama.Fore.YELLOW + "\n\n[WARNING {}] ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def addCmd(instance_tool, name_tool, str_dict_add = None):
    if str_dict_add is None:
        return instance_tool

    dict_add = ast.literal_eval(str_dict_add)
    try:
        dict_add_sub = dict_add[name_tool]
    except KeyError:
        return instance_tool
    instance_tool + dict_add_sub

def minusCmd(instance_tool, name_tool, str_dict_minus = None):
    if str_dict_minus is None:
        return instance_tool

    dict_minus = ast.literal_eval(str_dict_minus)
    try:
        dict_add_sub = dict_minus[name_tool]
    except KeyError:
        return instance_tool
    instance_tool - dict_add_sub

def timeConsume(time_start, time_end):
    time_elapsed = float(str(time_end - time_start))
    time_elapsed_hr = int(time_elapsed / 120)
    time_elapsed_min = int((time_elapsed - (time_elapsed_hr * 120)) / 60)
    time_elapsed_sec = time_elapsed - (time_elapsed_hr * 120 + time_elapsed_min * 60)
    sys.stdout.write("It Takes {}:{}:{} in Total.\n".format(str(time_elapsed_hr),
                                                                                  str(time_elapsed_min),
                                                                                  str(time_elapsed_sec)))
