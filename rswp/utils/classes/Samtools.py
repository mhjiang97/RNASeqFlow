from ..classes.Tools import *

class Samtools(Tools):
    def __init__(self, mode, common, settings):
        Tools.__init__(self, name = "SAMtools", common = common, settings = settings)
        self.mode = mode

    def action(self):
        bam = "{}/{}/{}.{}".format("/".join(self.settings.dir_bam),
                                   self.sample,
                                   self.sample,
                                   self.settings.suffix_bam)
        if self.mode == "index":
            self.cmds["indexing bam"] = "samtools index -@ {} {}".format(self.settings.nproc, bam)
            self.results["indexing bam"] = [bam + ".bai"]
