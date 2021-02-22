import sys, subprocess, os, time, colorama
import numpy as np
from ..utils import *
from collections import OrderedDict

colorama.init(autoreset = True)
def myNotification():
    sys.stdout.write(colorama.Fore.GREEN + "\n\n[NOTIFICATION {}] ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
def myError():
    sys.stderr.write(colorama.Fore.RED + "\n\n[ERROR {}] ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
def myWarning():
    sys.stdout.write(colorama.Fore.YELLOW + "\n\n[WARNING {}] ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

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
        myNotification()
        sys.stdout.write("Index is {} Running {} on {}\n".format(self.common.index, self.name, self.sample))

        if self.common.print_class:
            sys.stdout.write(str(self))

        myNotification()
        sys.stdout.write("All Commands Ready to Run in Queue:".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

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
                                myWarning()
                                sys.stdout.write("'{}' Exits! "
                                                 "Workflow will Quit!\n".format(result))
                                a[i] = True
                                #sys.exit(1)
                            else:
                                myWarning()
                                sys.stdout.write("'{}' Exits! But It's Empty! "
                                                 "Workflow Continues\n".format(result))
                        except FileNotFoundError:
                            continue
                        i += 1

                    if sum(a):
                        myError()
                        sys.stdout.write("Program Exits with Error!\n"
                                         "Remove '{}' and Run Again if You'd Like to Rerun {} on {}\n".format(" and ".join(np.array(self.results[cmd_name])[a]),
                                                                                                              self.name,
                                                                                                              self.sample))
                        sys.exit(1)
                except KeyError:
                    pass

            cmd = self.cmds[cmd_name]
            myNotification()
            sys.stdout.write("The Step Running is {}:\nCommand: {}\n".format(cmd_name, cmd))

            if self.common.run:
                subp = subprocess.Popen(cmd, shell = True,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE,
                                        encoding = "utf-8")
                #subp.wait()
                (out, err) = subp.communicate()
                myNotification()
                sys.stdout.write("stdout from {}:\n{}".format(cmd_name, out))
                myNotification()
                sys.stderr.write("stderr from {}:\n{}".format(cmd_name, err))
                if subp.poll() == 0:
                    myNotification()
                    sys.stdout.write("===== Step '{}' Finished Successfully! =====\n".format(cmd_name))
                else:
                    myError()
                    sys.stderr.write("***** Step '{}' Failed! *****\n".format(cmd_name))
                    sys.exit(1)
        sys.exit(0)

    def subSet(self, dict_default):
        self.__dict__ = mySub(dict_class = self.__dict__,
                              dict_yaml = self.common.returnSubSettings(self.name),
                              dict_default = dict_default)

    def createOut(self, name_tool_dir, out_type = "dir"):
        self.out = ""
        if out_type not in ["dir", "prefix"]:
            myError()
            sys.stderr.write("function createOut from class Tools "
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
        myNotification()
        return "The Tool Running is {}!\n" \
               "Class {} Attributes are:\n[{}: {}]\n".format(self.name,
                                                             self.name.capitalize(),
                                                             self.__class__.__name__,
                                                             self.gatherAttrs())

    def __add__(self, dict_cmd_add):
        for key in sorted(dict_cmd_add):
            try:
                self.cmds[key] = self.cmds[key] + " {}".format(dict_cmd_add[key])
            except KeyError:
                myError()
                sys.stderr.write("'{}' is not a correct command name of this tool. Please check it!".format(key))
                sys.exit(1)

    def __sub__(self, dict_cmd_del):
        for key in sorted(dict_cmd_del):
            self.cmds[key] = self.cmds[key].replace(" {}".format(dict_cmd_del[key]), "")
