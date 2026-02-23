import numpy as np

from .. import config
from ..utils import addCmd, minusCmd
from .base import Tools


class Samtools(Tools):
    def __init__(self, mode, common, settings):
        Tools.__init__(self, name="SAMtools", common=common, settings=settings)
        self.mode = mode

    def action(self):
        try:
            d_b = np.array(self.settings.dir_bam).flatten().tolist()
        except TypeError:
            d_b = self.settings.dir_bam
        bam = f"{'/'.join(d_b)}/{self.sample}/{self.sample}.{self.settings.suffix_bam}"
        if self.mode == "index":
            self.cmds["SAMtools indexing"] = f"samtools index -@ {self.settings.nproc} {bam}"
            self.results["SAMtools indexing"] = [bam + ".bai"]


def samtools(args, common, settings):
    mysamtools = Samtools(args.mode, common, settings)
    mysamtools.subSet(config.defaults_samtools)
    mysamtools.generateCmds()
    addCmd(mysamtools, mysamtools.name, mysamtools.common.add)
    minusCmd(mysamtools, mysamtools.name, mysamtools.common.sub)
    mysamtools.runCmds()
