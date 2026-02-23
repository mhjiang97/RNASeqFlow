import os

from .. import config
from ..utils import addCmd
from .base import Tools


class Fastqc(Tools):
    def __init__(self, name_fastqc_dir, common, settings):
        Tools.__init__(self, name="FastQC", common=common, settings=settings)
        self.name_fastqc_dir = name_fastqc_dir

    def action(self):
        self.out = f"{self.common.dir_project}/{self.name_fastqc_dir}/"
        file_in1 = f"{self.settings.dir_fq}/{self.sample}_R1.{self.settings.suffix_fq}"
        file_in2 = f"{self.settings.dir_fq}/{self.sample}_R2.{self.settings.suffix_fq}"
        if not os.path.exists(os.path.expanduser(self.out)):
            self.cmds["creating dir"] = f"mkdir -p {self.out}"
        self.cmds["quality controlling"] = f"fastqc -t {self.settings.nproc} -o {self.out} {file_in1} {file_in2}"

        self.results["quality controlling"] = [
            f"{self.out}/{self.sample}_R1_fastqc.html"
        ]
        self.results["quality controlling"].append(
            f"{self.out}/{self.sample}_R2_fastqc.html"
        )


def fastqc(args, common, settings):
    myfastqc = Fastqc(args.name_fastqc_dir, common, settings)
    myfastqc.subSet(config.defaults_fastqc)
    myfastqc.generateCmds()
    addCmd(myfastqc, myfastqc.name, myfastqc.common.add)
    myfastqc.runCmds()
