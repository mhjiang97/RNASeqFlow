import numpy as np
import yaml
from ..utils import *

class Common:
    def __init__(self, print_class, index, yaml_file, samples, dir_project, run, check):
        self.print_class = print_class
        self.index = index
        self.yaml_file = yaml_file
        self.samples = samples
        self.dir_project = dir_project
        self.run = run
        self.check = check

        self.dict_yaml = {}
        self.list_ids = []

    def loadYamlFile(self):
        self.dict_yaml = {}
        if self.yaml_file == "":
            return 0
        if self.yaml_file:
            y = yaml.load(self.yaml_file, Loader = yaml.FullLoader)
            self.dict_yaml.update(y)
            self.yaml_file.close()
        self.yaml_file = {"yaml_file":"dict loaded, closed and attribute unloaded"}

    def returnSubSettings(self, title):
        try:
            return self.dict_yaml[title]
        except KeyError:
            return {}

    def loadSampleIds(self):
        self.list_ids = []
        if self.samples is None:
            self.list_ids = []
            return 0
        if self.samples[0].endswith(".txt"):
            self.list_ids.extend(np.loadtxt(self.samples[0], dtype = "unicode_"))
        else:
            self.list_ids.extend(self.samples)

    def subSet(self, dict_default):
        self.__dict__ = mySub(dict_class = self.__dict__, dict_yaml = self.returnSubSettings("Common"), dict_default = dict_default)
