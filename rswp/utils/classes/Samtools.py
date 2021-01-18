from ..classes.Tools import *

class Samtools(Tools):
    def __init__(self, mode, common, settings):
        Tools.__init__(self, name = "SAMtools", common = common, settings = settings)
        self.mode = mode

    def action(self):
        try:
            d_b = np.array(self.settings.dir_bam).flatten().tolist()
        except TypeError:
            d_b = self.settings.dir_bam
        bam = "{}/{}/{}.{}".format("/".join(d_b), self.sample, self.sample, self.settings.suffix_bam)
        if self.mode == "index":
            self.cmds["SAMtools indexing"] = "samtools index -@ {} {}".format(self.settings.nproc, bam)
            self.results["SAMtools indexing"] = [bam + ".bai"]
