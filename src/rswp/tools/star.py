import sys

from .. import config
from ..utils import addCmd, minusCmd, myError
from .base import Tools


class Star(Tools):
    def __init__(
        self,
        build_index,
        dir_index,
        name_star_dir,
        transcript_bam,
        gene_counts,
        ram_bamsort,
        soft_clip,
        phred,
        common,
        settings,
    ):
        Tools.__init__(self, name="STAR", common=common, settings=settings)
        self.build_index = build_index
        self.dir_index = dir_index
        self.name_star_dir = name_star_dir
        self.transcript_bam = transcript_bam
        self.gene_counts = gene_counts
        self.ram_bamsort = ram_bamsort
        self.soft_clip = soft_clip
        self.phred = phred

    def action(self):
        self.createOut(self.name_star_dir)
        readfilescommand = "zcat" if self.settings.suffix_fq[-2:] == "gz" else "cat"
        file_in1 = f"{self.settings.dir_fq}/{self.sample}_R1.{self.settings.suffix_fq}"
        file_in2 = f"{self.settings.dir_fq}/{self.sample}_R2.{self.settings.suffix_fq}"
        if self.build_index:
            ##### build the commands dictionary #####
            self.cmds["building STAR index"] = (
                f"STAR "
                f"--runMode genomeGenerate "
                f"--runThreadN {self.settings.nproc} "
                f"--genomeDir {self.dir_index} "
                f"--genomeFastaFiles {self.settings.fa} "
                f"--sjdbGTFfile {self.settings.gtf}"
            )
        else:
            self.cmds["STAR mapping"] = (
                f"STAR "
                f"--runThreadN {self.settings.nproc} "
                f"--genomeDir {self.dir_index} "
                f"--readFilesIn {file_in1} {file_in2} "
                f"--readFilesCommand {readfilescommand} "
                f"--outFileNamePrefix {self.out} "
                f"--outSAMattrRGline ID:{self.sample} SM:{self.sample} LB:RNA PL:ILLUMINA "
                f"--sjdbGTFfile {self.settings.gtf} "
                f"--limitBAMsortRAM {self.ram_bamsort} "
                f"--outBAMsortingThreadN {self.settings.nproc} "
                f"--readQualityScoreBase {self.phred} "
                f"--outBAMcompression 10 "
                f"--sjdbOverhang 100 "
                f"--outSAMattrIHstart 0 "
                f"--outSAMtype BAM SortedByCoordinate "
                f"--outSAMattributes NH XS HI AS nM NM MD jM jI MC ch "
                f"--outSAMstrandField intronMotif "
                f"--twopassMode Basic"
            )

            self.cmds[
                "renaming the bam"
            ] = f"mv {self.out}/Aligned.sortedByCoord.out.bam {self.out}/{self.sample}.{self.settings.suffix_bam}"

            self.results["STAR mapping"] = [
                f"{self.out}/{self.sample}.{self.settings.suffix_bam}"
            ]


class StarTransBam(Star):
    def __init__(
        self,
        build_index,
        dir_index,
        name_star_dir,
        transcript_bam,
        gene_counts,
        ram_bamsort,
        soft_clip,
        phred,
        common,
        settings,
    ):
        Star.__init__(
            self,
            build_index=build_index,
            dir_index=dir_index,
            name_star_dir=name_star_dir,
            transcript_bam=transcript_bam,
            gene_counts=gene_counts,
            ram_bamsort=ram_bamsort,
            soft_clip=soft_clip,
            phred=phred,
            common=common,
            settings=settings,
        )

    def action(self):
        if self.build_index:
            myError(
                "transcript_bam and build_index are mutually exclusive!!"
                "\nPlease delete flag transcript_bam if you want to build a star index!!\n"
            )
            sys.exit(1)
        else:
            Star.action(self)
            self.cmds["STAR mapping"] = (
                self.cmds["STAR mapping"] + " --quantMode TranscriptomeSAM"
            )
            self.cmds["renaming the transcript bam"] = (
                f"mv {self.out}/Aligned.toTranscriptome.out.bam "
                f"{self.out}/{self.sample}.Transcriptome.bam"
            )

            self.results["STAR mapping"].append(
                f"{self.out}/{self.sample}.Transcriptome.bam"
            )


def star(args, common, settings):
    if args.transcript_bam is None:
        tb = config.defaults_star["transcript_bam"]
        try:
            tb = common.returnSubSettings("STAR")["transcript_bam"]
        except KeyError:
            pass
    else:
        tb = args.transcript_bam

    if tb:
        mystar = StarTransBam(
            args.build_index,
            args.dir_index,
            args.name_star_dir,
            args.transcript_bam,
            args.gene_counts,
            args.ram_bamsort,
            args.soft_clip,
            args.phred,
            common,
            settings,
        )
    else:
        mystar = Star(
            args.build_index,
            args.dir_index,
            args.name_star_dir,
            args.transcript_bam,
            args.gene_counts,
            args.ram_bamsort,
            args.soft_clip,
            args.phred,
            common,
            settings,
        )
    mystar.subSet(config.defaults_star)
    mystar.generateCmds()
    if mystar.gene_counts:
        if tb:
            mystar - dict(zip(["STAR mapping"], ["--quantMode TranscriptomeSAM"]))
            mystar + dict(
                zip(["STAR mapping"], ["--quantMode TranscriptomeSAM GeneCounts"])
            )
        else:
            mystar + dict(zip(["STAR mapping"], ["--quantMode GeneCounts"]))
    if not mystar.soft_clip:
        mystar + dict(zip(["STAR mapping"], ["--alignEndsType EndToEnd"]))
    addCmd(mystar, mystar.name, mystar.common.add)
    minusCmd(mystar, mystar.name, mystar.common.sub)
    mystar.runCmds()
