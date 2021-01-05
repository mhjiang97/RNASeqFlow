from ..classes.Tools import *

class Rsem(Tools):
    def __init__(self, prepare_reference, prefix_reference, name_rsem_dir, common, settings):
        Tools.__init__(self, name = "RSEM", common = common, settings = settings)
        self.prepare_reference = prepare_reference
        self.prefix_reference = prefix_reference
        self.name_rsem_dir = name_rsem_dir

    def action(self):
        if self.prepare_reference:
            if not os.path.exists(os.path.dirname(self.prefix_reference)):
                self.cmds["creating dir"] = "mkdir -p {}".format(os.path.dirname(self.prefix_reference))
            self.cmds["preparing RSEM reference"] = "rsem-prepare-reference " \
                                                    "--gtf {} " \
                                                    "{} " \
                                                    "{}".format(self.settings.gtf,
                                                                self.settings.fa,
                                                                self.prefix_reference)
        else:
            bam = "{}/{}/{}.Transcriptome.bam".format("/".join(self.settings.dir_bam),
                                                            self.sample,
                                                            self.sample)
            self.createOut(self.name_rsem_dir)
            if not os.path.exists(os.path.expanduser(self.out)):
                self.cmds["creating dir"] = "mkdir -p {}".format(self.out)
            self.createOut(self.name_rsem_dir, out_type = "prefix")
            self.cmds["RSEM quantification"] = "rsem-calculate-expression " \
                                               "--paired-end " \
                                               "--alignments " \
                                               "--no-bam-output " \
                                               "-p {} " \
                                               "{} " \
                                               "{} " \
                                               "{}".format(self.settings.nproc,
                                                           bam,
                                                           self.prefix_reference,
                                                           self.out)

            self.results["RSEM quantification"] = ["{}.genes.results".format(self.out)]
            self.results["RSEM quantification"].append("{}.isoforms.results".format(self.out))
