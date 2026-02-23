import os

import numpy as np

from .. import config
from ..utils import addCmd, minusCmd
from .base import Tools


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
                self.cmds["creating dir"] = f"mkdir -p {os.path.dirname(self.prefix_reference)}"
            self.cmds["preparing RSEM reference"] = (
                f"rsem-prepare-reference "
                f"--gtf {self.settings.gtf} "
                f"{self.settings.fa} "
                f"{self.prefix_reference}"
            )
        else:
            try:
                d_b = np.array(self.settings.dir_bam).flatten().tolist()
            except TypeError:
                d_b = self.settings.dir_bam
            bam = f"{'/'.join(d_b)}/{self.sample}/{self.sample}.Transcriptome.bam"
            self.createOut(self.name_rsem_dir)
            if not os.path.exists(os.path.expanduser(self.out)):
                self.cmds["creating dir"] = f"mkdir -p {self.out}"
            self.createOut(self.name_rsem_dir, out_type="prefix")
            self.cmds["RSEM quantification"] = (
                f"rsem-calculate-expression "
                f"--paired-end "
                f"--alignments "
                f"--no-bam-output "
                f"-p {self.settings.nproc} "
                f"{bam} "
                f"{self.prefix_reference} "
                f"{self.out}"
            )

            self.results["RSEM quantification"] = [f"{self.out}.genes.results"]
            self.results["RSEM quantification"].append(
                f"{self.out}.isoforms.results"
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
            ] + f" --bowtie2 --bowtie2-path {self.path_bowtie2}"
        else:
            # if self.settings.suffix_fq.endswith("gz"):
            #    myError("\n\nError: bowtie2 can't handle compressed files! "
            #                     "Please decompress them and run again.\n")
            #    sys.exit(1)
            file_in1 = f"{self.settings.dir_fq}/{self.sample}_R1.{self.settings.suffix_fq}"
            file_in2 = f"{self.settings.dir_fq}/{self.sample}_R2.{self.settings.suffix_fq}"
            self.createOut(self.name_rsem_dir)
            dt = os.path.dirname(os.path.abspath(os.path.expanduser(self.out)))
            if not os.path.exists(os.path.expanduser(dt + "/bowtie2/")):
                self.cmds["creating dir"] = f"mkdir -p {dt}/bowtie2/"
            self.cmds["RSEM quantification"] = (
                f"rsem-calculate-expression "
                f"--paired-end "
                f"--bowtie2 "
                f"--seed 123 "
                f"--bowtie2-path {self.path_bowtie2} "
                f"-p {self.settings.nproc} "
                f"{file_in1} {file_in2} "
                f"{self.prefix_reference} "
                f"{dt}/bowtie2/{self.sample}"
            )

            self.results["RSEM quantification"] = [
                f"{dt}/bowtie2/{self.sample}.genes.results"
            ]
            self.results["RSEM quantification"].append(
                f"{dt}/bowtie2/{self.sample}.isoforms.results"
            )


def rsem(args, common, settings):
    if args.fq is None:
        fq = config.defaults_rsem["fq"]
        try:
            fq = common.returnSubSettings("RSEM")["fq"]
        except KeyError:
            pass
    else:
        fq = args.fq

    if fq:
        myrsem = RsemBowtie2(
            args.fq,
            args.path_bowtie2,
            args.prepare_reference,
            args.prefix_reference,
            args.name_rsem_dir,
            common,
            settings,
        )
    else:
        myrsem = Rsem(
            args.fq,
            args.path_bowtie2,
            args.prepare_reference,
            args.prefix_reference,
            args.name_rsem_dir,
            common,
            settings,
        )
    myrsem.subSet(config.defaults_rsem)
    myrsem.generateCmds()
    addCmd(myrsem, myrsem.name, myrsem.common.add)
    minusCmd(myrsem, myrsem.name, myrsem.common.sub)
    myrsem.runCmds()
