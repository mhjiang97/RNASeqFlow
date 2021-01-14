from ..classes.Tools import *

class Star(Tools):
    def __init__(self, build_index, dir_index, name_star_dir,
                 transcript_bam, ram_bamsort, soft_clip,
                 phred, common, settings):
        Tools.__init__(self, name = "STAR", common = common, settings = settings)
        self.build_index = build_index
        self.dir_index = dir_index
        self.name_star_dir = name_star_dir
        self.transcript_bam = transcript_bam
        self.ram_bamsort = ram_bamsort
        self.soft_clip = soft_clip
        self.phred = phred

    def action(self):
        self.createOut(self.name_star_dir)
        readfilescommand = "zcat" if self.settings.suffix_fq[-2:] == "gz" else "cat"
        file_in1 = "{}/{}_R1.{}".format(self.settings.dir_fq,
                                        self.sample,
                                        self.settings.suffix_fq)
        file_in2 = "{}/{}_R2.{}".format(self.settings.dir_fq,
                                        self.sample,
                                        self.settings.suffix_fq)
        if self.build_index:
            ##### build the commands dictionary #####
            self.cmds["building STAR index"] = "STAR " \
                                               "--runMode genomeGenerate " \
                                               "--runThreadN {} " \
                                               "--genomeDir {} " \
                                               "--genomeFastaFiles {} " \
                                               "--sjdbGTFfile {}".format(self.settings.nproc,
                                                                         self.dir_index,
                                                                         self.settings.fa,
                                                                         self.settings.gtf)
        else:
            self.cmds["STAR mapping"] = "STAR " \
                                        "--runThreadN {} " \
                                        "--genomeDir {} " \
                                        "--readFilesIn {} {} " \
                                        "--readFilesCommand {} " \
                                        "--outFileNamePrefix {} " \
                                        "--outSAMattrRGline ID:{} SM:{} LB:RNA PL:ILLUMINA " \
                                        "--sjdbGTFfile {} " \
                                        "--limitBAMsortRAM {} " \
                                        "--outBAMsortingThreadN {}" \
                                        "--readQualityScoreBase {} " \
                                        "--outBAMcompression 10 " \
                                        "--sjdbOverhang 100 " \
                                        "--outSAMtype BAM SortedByCoordinate " \
                                        "--outSAMattributes NH XS HI AS nM NM MD jM jI MC ch " \
                                        "--twopassMode Basic".format(self.settings.nproc,
                                                                     self.dir_index,
                                                                     file_in1,
                                                                     file_in2,
                                                                     readfilescommand,
                                                                     self.out,
                                                                     self.sample,
                                                                     self.sample,
                                                                     self.settings.gtf,
                                                                     self.ram_bamsort,
                                                                     self.settings.nproc,
                                                                     self.phred)

            self.cmds["renaming the bam"] = "mv {}/Aligned.sortedByCoord.out.bam " \
                                            "{}/{}.{}".format(self.out,
                                                              self.out,
                                                              self.sample,
                                                              self.settings.suffix_bam)

            self.results["STAR mapping"] = ["{}/{}.{}".format(self.out, self.sample, self.settings.suffix_bam)]


class StarTransBam(Star):
    def __init__(self, build_index, dir_index, name_star_dir,
                 transcript_bam, ram_bamsort, soft_clip,
                 phred, common, settings):
        Star.__init__(self, build_index = build_index, dir_index = dir_index, name_star_dir = name_star_dir,
                      transcript_bam = transcript_bam, ram_bamsort = ram_bamsort, soft_clip = soft_clip,
                      phred = phred, common = common, settings = settings)
    def action(self):
        if self.build_index:
            myError()
            sys.stderr.write("transcript_bam and build_index are mutually exclusive!!"
                             "\nPlease delete flag transcript_bam if you want to build a star index!!\n")
            sys.exit(1)
        else:
            Star.action(self)
            self.cmds["STAR mapping"] = self.cmds["STAR mapping"] + " --quantMode TranscriptomeSAM GeneCounts"
            self.cmds["renaming the transcript bam"] = "mv {}/Aligned.toTranscriptome.out.bam " \
                                                       "{}/{}.Transcriptome.bam".format(self.out,
                                                                                        self.out,
                                                                                        self.sample)

            self.results["STAR mapping"].append("{}/{}.Transcriptome.bam".format(self.out, self.sample))
