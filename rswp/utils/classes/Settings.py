import numpy as np
from ..utils import *

class Settings:
    def __init__(self, nproc, gtf, fa, suffix_fq, suffix_bam, dir_fq, dir_bam):
        self.nproc = nproc
        self.gtf = gtf
        self.fa = fa
        self.suffix_fq = suffix_fq
        self.suffix_bam = suffix_bam
        self.dir_fq = dir_fq
        try:
            self.dir_bam = np.array(dir_bam).flatten().tolist()
        except TypeError:
            self.dir_bam = dir_bam

    def subSet(self, common, dict_default):
        self.__dict__ = mySub(dict_class = self.__dict__,
                              dict_yaml = common.returnSubSettings("Settings"),
                              dict_default = dict_default)

