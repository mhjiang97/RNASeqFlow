from .. import config
from ..utils import addCmd, minusCmd
from .base import Tools


class Salmon(Tools):
    def __init__(self, dir_index, name_salmon_dir, common, settings):
        Tools.__init__(self, name="Salmon", common=common, settings=settings)
        self.dir_index = dir_index
        self.name_salmon_dir = name_salmon_dir

    def action(self):
        self.createOut(self.name_salmon_dir)
        file_in1 = f"{self.settings.dir_fq}/{self.sample}_R1.{self.settings.suffix_fq}"
        file_in2 = f"{self.settings.dir_fq}/{self.sample}_R2.{self.settings.suffix_fq}"
        self.cmds["Salmon quantification"] = (
            f"salmon quant -l A "
            f"-p {self.settings.nproc} "
            f"-i {self.dir_index} "
            f"--geneMap {self.settings.gtf} "
            f"-1 {file_in1} "
            f"-2 {file_in2} "
            f"-o {self.out} "
            f"--validateMappings "
            f"--gcBias "
            f"--seqBias"
        )

        self.cmds["Compressing the sf file"] = f"gzip {self.out}/quant.sf"

        if self.settings.gtf is not None:
            self.cmds["Compressing the gene sf file"] = f"gzip {self.out}/quant.genes.sf"

        self.results["Salmon quantification"] = [f"{self.out}/quant.sf.gz"]
        if self.settings.gtf is not None:
            self.results["Salmon gene quantification"] = [
                f"{self.out}/quant.genes.sf.gz"
            ]


def salmon(args, common, settings):
    mysalmon = Salmon(args.dir_index, args.name_salmon_dir, common, settings)
    mysalmon.subSet(config.defaults_salmon)
    mysalmon.generateCmds()
    addCmd(mysalmon, mysalmon.name, mysalmon.common.add)
    minusCmd(mysalmon, mysalmon.name, mysalmon.common.sub)
    if mysalmon.settings.gtf is None:
        mysalmon - {"Salmon quantification": "--geneMap None"}
    mysalmon.runCmds()
