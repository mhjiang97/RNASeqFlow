import os
import subprocess
import sys
import time
from collections import OrderedDict

import colorama
import numpy as np

from ..utils import myError, myNotification, mySub, myWarning, timeConsume

colorama.init(autoreset=True)


class Tools:
    def __init__(self, name, common, settings):
        self.name = name
        self.common = common
        self.settings = settings

        self.cmds = OrderedDict()
        self.out = ""
        self.results = {}
        ##### It's better to place the assignment statement in a certain function chunk! #####
        try:
            self.sample = self.common.list_ids[self.common.index - 1]
        except IndexError:
            self.sample = "no_sample"

    def generateCmds(self, *values):
        return self.action(*values)

    def action(self):
        raise NotImplementedError("action must be defined in subclasses!")

    def runCmds(self):
        myNotification(
            f"Index is {self.common.index} Running {self.name} on {self.sample}\n"
        )

        if self.common.print_class:
            myNotification(str(self))

        myNotification("All Commands Ready to Run in Queue:")

        for cmd_name in self.cmds.keys():
            myNotification(f"\n{cmd_name}: {self.cmds[cmd_name]}\n")

        for cmd_name in self.cmds.keys():
            if self.common.check:
                try:
                    a = np.zeros(len(self.results[cmd_name]), dtype=bool)
                    for i, result in enumerate(self.results[cmd_name]):
                        try:
                            size = os.path.getsize(os.path.expanduser(result))
                            if size > 0:
                                myWarning(
                                    f"'{result}' Exits! "
                                    "Workflow Will Quit!\n"
                                )
                                a[i] = True
                                # sys.exit(1)
                            else:
                                myWarning(
                                    f"'{result}' Exits! But It's Empty! "
                                    "Workflow Continues\n"
                                )
                        except FileNotFoundError:
                            continue

                    if a.any():
                        failed_results = " and ".join(np.array(self.results[cmd_name])[a])
                        myError(
                            "Program Exits With Error!\n"
                            f"Remove '{failed_results}' and Run Again "
                            f"if You'd Like to Rerun {self.name} on {self.sample}\n"
                        )
                        sys.exit(1)
                except KeyError:
                    pass

            cmd = self.cmds[cmd_name]
            myNotification(
                f"The Step Running is {cmd_name}:\nCommand: {cmd}\n"
            )

            if self.common.run:
                time_start = time.time()
                subp = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding="utf-8",
                )
                # subp.wait()
                (out, err) = subp.communicate()
                myNotification(f"Stdout From {cmd_name}:\n{out}")
                myNotification(f"Stderr From {cmd_name}:\n{err}")
                if subp.poll() == 0:
                    myNotification(
                        f"==== Step '{cmd_name}' Finished Successfully! ====\n"
                    )
                    time_success = time.time()
                    timeConsume(time_start, time_success)
                else:
                    myError(f"**** Step '{cmd_name}' Failed! ****\n")
                    time_fail = time.time()
                    timeConsume(time_start, time_fail)
                    sys.exit(1)
        sys.exit(0)

    def subSet(self, dict_default):
        self.__dict__ = mySub(
            dict_class=self.__dict__,
            dict_yaml=self.common.returnSubSettings(self.name),
            dict_default=dict_default,
        )

    def createOut(self, name_tool_dir, out_type="dir"):
        self.out = ""
        if out_type not in ["dir", "prefix"]:
            myError(
                "function createOut from class Tools "
                "only accept 'dir' or 'prefix' for 'out_type' argument\n"
                f"please modify the source code for class {self.name}\n"
            )
            sys.exit(1)

        o = f"{self.common.dir_project}/{name_tool_dir}/{self.sample}/"  # self.common.list_ids[self.common.index - 1]
        if out_type == "prefix":
            o = o + self.sample  # self.common.list_ids[self.common.index - 1]
        self.out = self.out + o

    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append(f"{key} = {getattr(self, key)}")
        return ", ".join(attrs)

    def __str__(self):
        return (
            f"The Tool Running is {self.name}!\n"
            f"Class {self.name.capitalize()} Attributes are:\n[{self.__class__.__name__}: {self.gatherAttrs()}]\n"
        )

    def __add__(self, dict_cmd_add):
        for key in sorted(dict_cmd_add):
            try:
                self.cmds[key] = self.cmds[key] + f" {dict_cmd_add[key]}"
            except KeyError:
                myError(
                    f"""'{key}' isn't a Correct Command Name of This Tool.\nAddition '+' can't be Calculated.\nPlease Check It!\n"""
                )
                sys.exit(1)
        return self

    def __sub__(self, dict_cmd_del):
        for key in sorted(dict_cmd_del):
            try:
                self.cmds[key] = self.cmds[key].replace(
                    f" {dict_cmd_del[key]}", ""
                )
            except KeyError:
                myError(
                    f"""'{key}' isn't a Correct Command Name of This Tool.\nSubtraction '-' can't be Calculated.\nPlease Check It!\n"""
                )
                sys.exit(1)
        return self
