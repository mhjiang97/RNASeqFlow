from ..classes.Tools import *


class Salmon(Tools):
    def __init__(self, dir_index, name_salmon_dir, common, settings):
        Tools.__init__(self, name="Salmon", common=common, settings=settings)
        self.dir_index = dir_index
        self.name_salmon_dir = name_salmon_dir

    def action(self):
        self.createOut(self.name_salmon_dir)
        file_in1 = "{}/{}_R1.{}".format(
            self.settings.dir_fq, self.sample, self.settings.suffix_fq
        )
        file_in2 = "{}/{}_R2.{}".format(
            self.settings.dir_fq, self.sample, self.settings.suffix_fq
        )
        self.cmds["Salmon quantification"] = (
            "salmon quant -l A "
            "-p {} "
            "-i {} "
            "--geneMap {} "
            "-1 {} "
            "-2 {} "
            "-o {} "
            "--validateMappings "
            "--gcBias "
            "--seqBias".format(
                self.settings.nproc,
                self.dir_index,
                self.settings.gtf,
                file_in1,
                file_in2,
                self.out,
            )
        )

        self.cmds["Compressing the sf file"] = "gzip {}/quant.sf".format(self.out)

        if not self.settings.gtf is None:
            self.cmds["Compressing the gene sf file"] = "gzip {}/quant.genes.sf".format(
                self.out
            )

        self.results["Salmon quantification"] = ["{}/quant.sf.gz".format(self.out)]
        if not self.settings.gtf is None:
            self.results["Salmon gene quantification"] = [
                "{}/quant.genes.sf.gz".format(self.out)
            ]
