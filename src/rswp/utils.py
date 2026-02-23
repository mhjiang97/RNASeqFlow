import argparse
import ast
import copy
import logging
import sys
import time

import colorama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def newSubparser():
    return argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.RawTextHelpFormatter
    )


def mySub(dict_class, dict_yaml, dict_default):
    mydict = copy.deepcopy(dict_class)
    for key, value in mydict.items():
        if value is None and key in dict_yaml:
            mydict[key] = dict_yaml[key]

    for attr, value in dict_default.items():
        if attr in mydict and mydict[attr] is None:
            mydict[attr] = value

    return mydict


def myNotification(msg=""):
    logger.info(
        colorama.Fore.GREEN
        + f"\n\n[NOTIFICATION {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    )


def myError(msg=""):
    logger.error(
        colorama.Fore.RED
        + f"\n\n[ERROR {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    )


def myWarning(msg=""):
    logger.warning(
        colorama.Fore.YELLOW
        + f"\n\n[WARNING {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    )


def addCmd(instance_tool, name_tool, str_dict_add=None):
    if str_dict_add is None:
        return instance_tool

    dict_add = ast.literal_eval(str_dict_add)
    if name_tool not in dict_add:
        return instance_tool

    instance_tool = instance_tool + dict_add[name_tool]
    return instance_tool


def minusCmd(instance_tool, name_tool, str_dict_minus=None):
    if str_dict_minus is None:
        return instance_tool

    dict_minus = ast.literal_eval(str_dict_minus)
    if name_tool not in dict_minus:
        return instance_tool

    instance_tool = instance_tool - dict_minus[name_tool]
    return instance_tool


def timeConsume(time_start, time_end):
    time_elapsed = time_end - time_start
    time_elapsed_hr = int(time_elapsed // 3600)
    time_elapsed_min = int((time_elapsed % 3600) // 60)
    time_elapsed_sec = time_elapsed % 60
    logger.info(
        f"It Takes {time_elapsed_hr:02d}:{time_elapsed_min:02d}:{time_elapsed_sec:05.2f} in Total.\n"
    )
