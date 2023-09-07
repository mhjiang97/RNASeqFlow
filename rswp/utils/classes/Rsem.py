from ..classes.Tools import *


class Rsem(Tools):
    def __init__(
        self,
        fq,
        path_bowtie2,
        prepare_reference,
        prefix_reference,
        name_rsem_dir,
        common,
        settings,
    ):
        Tools.__init__(self, name="RSEM", common=common, settings=settings)
        self.fq = fq
        self.path_bowtie2 = path_bowtie2
        self.prepare_reference = prepare_reference
        self.prefix_reference = prefix_reference
        self.name_rsem_dir = name_rsem_dir

    def action(self):
        if self.prepare_reference:
            if not os.path.exists(os.path.dirname(self.prefix_reference)):
                self.cmds["creating dir"] = "mkdir -p {}".format(
                    os.path.dirname(self.prefix_reference)
                )
            self.cmds["preparing RSEM reference"] = (
                "rsem-prepare-reference "
                "--gtf {} "
                "{} "
                "{}".format(self.settings.gtf, self.settings.fa, self.prefix_reference)
            )
        else:
            try:
                d_b = np.array(self.settings.dir_bam).flatten().tolist()
            except TypeError:
                d_b = self.settings.dir_bam
            bam = "{}/{}/{}.Transcriptome.bam".format(
                "/".join(d_b), self.sample, self.sample
            )
            self.createOut(self.name_rsem_dir)
            if not os.path.exists(os.path.expanduser(self.out)):
                self.cmds["creating dir"] = "mkdir -p {}".format(self.out)
            self.createOut(self.name_rsem_dir, out_type="prefix")
            self.cmds["RSEM quantification"] = (
                "rsem-calculate-expression "
                "--paired-end "
                "--alignments "
                "--no-bam-output "
                "-p {} "
                "{} "
                "{} "
                "{}".format(self.settings.nproc, bam, self.prefix_reference, self.out)
            )

            self.results["RSEM quantification"] = ["{}.genes.results".format(self.out)]
            self.results["RSEM quantification"].append(
                "{}.isoforms.results".format(self.out)
            )


class RsemBowtie2(Rsem):
    def __init__(
        self,
        fq,
        path_bowtie2,
        prepare_reference,
        prefix_reference,
        name_rsem_dir,
        common,
        settings,
    ):
        Rsem.__init__(
            self,
            fq,
            path_bowtie2,
            prepare_reference,
            prefix_reference,
            name_rsem_dir,
            common,
            settings,
        )

    def action(self):
        if self.prepare_reference:
            Rsem.action(self)
            self.cmds["preparing RSEM reference"] = self.cmds[
                "preparing RSEM reference"
            ] + " --bowtie2 --bowtie2-path {}".format(self.path_bowtie2)
        else:
            # if self.settings.suffix_fq.endswith("gz"):
            #    sys.stderr.write("\n\nError: bowtie2 can't handle compressed files! "
            #                     "Please decompress them and run again.\n")
            #    sys.exit(1)
            file_in1 = "{}/{}_R1.{}".format(
                self.settings.dir_fq, self.sample, self.settings.suffix_fq
            )
            file_in2 = "{}/{}_R2.{}".format(
                self.settings.dir_fq, self.sample, self.settings.suffix_fq
            )
            self.createOut(self.name_rsem_dir)
            dt = os.path.dirname(os.path.abspath(os.path.expanduser(self.out)))
            if not os.path.exists(os.path.expanduser(dt + "/bowtie2/")):
                self.cmds["creating dir"] = "mkdir -p {}".format(dt + "/bowtie2/")
            self.cmds["RSEM quantification"] = (
                "rsem-calculate-expression "
                "--paired-end "
                "--bowtie2 "
                "--seed 123 "
                "--bowtie2-path {} "
                "-p {} "
                "{} {} "
                "{} "
                "{}/bowtie2/{}".format(
                    self.path_bowtie2,
                    self.settings.nproc,
                    file_in1,
                    file_in2,
                    self.prefix_reference,
                    dt,
                    self.sample,
                )
            )

            self.results["RSEM quantification"] = [
                "{}/bowtie2/{}.genes.results".format(dt, self.sample)
            ]
            self.results["RSEM quantification"].append(
                "{}/bowtie2/{}.isoforms.results".format(dt, self.sample)
            )
