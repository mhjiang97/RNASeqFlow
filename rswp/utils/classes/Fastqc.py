from ..classes.Tools import *

class Fastqc(Tools):
    def __init__(self, name_fastqc_dir, common, settings):
        Tools.__init__(self, name = "FastQC", common = common, settings = settings)
        self.name_fastqc_dir = name_fastqc_dir

    def action(self):
        self.out = "{}/{}/".format(self.common.dir_project, self.name_fastqc_dir)
        file_in1 = "{}/{}_R1.{}".format(self.settings.dir_fq,
                                        self.sample,
                                        self.settings.suffix_fq)
        file_in2 = "{}/{}_R2.{}".format(self.settings.dir_fq,
                                        self.sample,
                                        self.settings.suffix_fq)
        if not os.path.exists(os.path.expanduser(self.out)):
            self.cmds["creating dir"] = "mkdir -p {}".format(self.out)
        self.cmds["fastqc"] = "fastqc -t {} -o {} {} {}".format(self.settings.nproc, self.out, file_in1, file_in2)

        self.results["fastqc"] = ["{}/{}_R1_fastqc.html".format(self.out, self.sample)]
        self.results["fastqc"].append("{}/{}_R2_fastqc.html".format(self.out, self.sample))
