import sys, subprocess, os
import numpy as np
from ..utils import *
from collections import OrderedDict

class Tools:
    def __init__(self, name, common, settings):
        self.name = name
        self.common = common
        self.settings = settings

        self.cmds = OrderedDict()
        self.out = ""
        self.results = {}
        ##### it's better to place the assignment statement in a certain function chunk! #####
        try:
            self.sample = self.common.list_ids[self.common.index - 1]
        except IndexError:
            self.sample = "no_sample"

    def generateCmds(self, *values):
        return self.action(*values)

    def action(self):
        assert False, 'action must be defined in subclasses!'

    def runCmds(self):
        sys.stdout.write("\n\n[NOTIFICATION] Index is {}. Running {} on {}\n".format(self.common.index, self.name, self.sample))
        if self.common.print_class:
            sys.stdout.write(str(self))
        sys.stdout.write("\n\n[NOTIFICATION] All Commands Ready to Run in Queue:")

        for cmd_name in self.cmds.keys():
            sys.stdout.write("\n{}: {}\n".format(cmd_name, self.cmds[cmd_name]))

        for cmd_name in self.cmds.keys():
            if self.common.check:
                i = 0
                try:
                    a = np.array([False]).repeat(len(self.results[cmd_name]))
                    for result in self.results[cmd_name]:
                        try:
                            size = os.path.getsize(os.path.expanduser(result))
                            if size > 0:
                                sys.stdout.write("\n\n[WARNING] '{}' Exits! "
                                                 "Workflow will Quit!\n".format(result))
                                a[i] = True
                                #sys.exit(1)
                            else:
                                sys.stdout.write("\n\n[WARNING] '{}' Exits! But It's Empty! "
                                                 "Workflow Continues\n".format(result))
                        except FileNotFoundError:
                            continue
                        i += 1

                    if sum(a):
                        sys.stdout.write("\n\n[NOTIFICATION] Remove '{}' "
                                         "and Run Again if You'd Like to Rerun {} on {}\n"
                                         "\nProgram Exits with Error!\n".format(" and ".join(np.array(self.results[cmd_name])[a]),
                                                                                self.name,
                                                                                self.sample))
                        sys.exit(1)
                except KeyError:
                    pass

            cmd = self.cmds[cmd_name]
            sys.stdout.write("\n\n[NOTIFICATION] The Step Running is: {}.\nThe Command is: {}\n".format(cmd_name, cmd))

            if self.common.run:
                subp = subprocess.Popen(cmd, shell = True,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE,
                                        encoding = "utf-8")
                #subp.wait()
                (out, err) = subp.communicate()
                sys.stdout.write("\n\n[NOTIFICATION] stdout from {} :\n{}".format(cmd_name, out))
                sys.stderr.write("\n\n[NOTIFICATION] stderr from {} :\n{}".format(cmd_name, err))
                if subp.poll() == 0:
                    sys.stdout.write("\n\n===== [NOTIFICATION] Step '{}' Finished Successfully! =====\n".format(cmd_name))
                else:
                    sys.stderr.write("\n\n***** [ERROR] Step '{}' Failed! *****\n".format(cmd_name))
                    sys.exit(1)
        sys.exit(0)

    def subSet(self, dict_default):
        self.__dict__ = mySub(dict_class = self.__dict__,
                              dict_yaml = self.common.returnSubSettings(self.name),
                              dict_default = dict_default)

    def createOut(self, name_tool_dir, out_type = "dir"):
        self.out = ""
        if out_type not in ["dir", "prefix"]:
            sys.stderr.write("\n\n[ERROR] function createOut from class Tools "
                             "only accept 'dir' or 'prefix' for 'out_type' argument\n"
                             "please modify the source code for class {}\n".format(self.name))
            sys.exit(1)

        o = "{}/{}/{}/".format(self.common.dir_project,
                               name_tool_dir,
                               self.sample) # self.common.list_ids[self.common.index - 1]
        if out_type == "prefix":
            o = o + self.sample # self.common.list_ids[self.common.index - 1]
        self.out = self.out + o

    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append("{} = {}".format(key, getattr(self, key)))
        return ", ".join(attrs)

    def __str__(self):
        return "\n\n[NOTIFICATION] The Tool Running is {}!\n" \
               "Class {} Attributes are:\n[{}: {}]\n".format(self.name,
                                                             self.name.capitalize(),
                                                             self.__class__.__name__,
                                                             self.gatherAttrs())

    def __add__(self, dict_cmd_add):
        for key in sorted(dict_cmd_add):
            self.cmds[key] = self.cmds[key] + " {}".format(dict_cmd_add[key])
