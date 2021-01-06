#!/usr/bin/env python

import sys, textwrap
from utils.functions import *
from utils.classes import *
from utils import defaults
from utils.utils import *

version = "0.0.0.9000"

def main():
    # ===================================================================================== #
    # note: give up the setting defaults method under argparse in order to fulfill the aim  #
    # manipulating between yaml file settings and command line parameters at will           #
    #====================================================================================== #

    ## ----- top-level parser ----- ##
    parser_top = argparse.ArgumentParser(usage = "%(prog)s 【version: {}】".format(version),
    description = textwrap.dedent("""\
    ===== ---------------------------- =====
    ##### Python Workflow for RNA-seq  #####
    ===== ---------------------------- =====
    """),epilog = textwrap.dedent("""\
    ===================================================================================
    Feel Free to Contact Minghao Jiang via jiamginghao1001@163.com When Having Troubles
    ===================================================================================
    """), formatter_class = argparse.RawTextHelpFormatter)
    parser_top.add_argument("-v", "--version", action = "version", version = version)

    parser_groups = newSubparser()
    ## ----- common parser ----- ##
    parser_common = parser_groups.add_argument_group(title = textwrap.dedent("COMMON SETTINGS"),
                                                     description = textwrap.dedent("*** WARNING: parameters having default values will always be prior to themselves defined in the config file ***"))
    parser_common.add_argument("--print_class", action = argparse.BooleanOptionalAction, default = None,
                               help = "print tool classes details before running commands or not")
    parser_common.add_argument("-i", "--index", type = int, metavar = "1, 2, 3, ...",
                               help = "which sample to run. "
                                      "[Default: {}] means run the first sample.This parameter will be very useful when being in a loop".format(defaults.defaults_common["index"]))
    parser_common.add_argument("-c", "--config", dest = "yaml_file", type = argparse.FileType('r'), metavar = "~/projects/bcpall/doc/config.yaml",
                               help = "a config file in yaml format having 2 hierarchies. "
                                      "No default value, so complement all non-default parameters if you don't have one")
    parser_common.add_argument("-s", "--samples", nargs = "+", metavar = ('samples.txt', 'id'),
                               help = "either a file incorporating sample ids without a header or a list of sample ids")
    parser_common.add_argument("-d", "--dir_project", type = str, metavar = "~/projects/bcpall/analysis/rnaseq",
                               help = "use the dir as prefix of outputs. "
                                      "[Default: {}] means workflow yields output in the current dir".format(defaults.defaults_common["dir_project"]))
    parser_common.add_argument("--run", action = argparse.BooleanOptionalAction, default = None,
                               help = "run shell scripts or only print them on the screen")
    parser_common.add_argument("--check", action = argparse.BooleanOptionalAction, default = None,
                               help = "if result files exit program will exit with an error")

    ## ----- paths or necessary files settings ----- ##
    parser_settings = parser_groups.add_argument_group(title = "PATHS SETTINGS",
                                                       description = textwrap.dedent("*** aiming at substituting for defined paths in the config file ***"))
    parser_settings.add_argument("-j", "--nproc", type = int,
                                 help ="number of threads. "
                                       "[Default: {}]".format(defaults.defaults_settings["nproc"]))
    parser_settings.add_argument("--gtf", type = str, help = "a preferred gtf file")
    parser_settings.add_argument("--fa", type = str, help = "a preferred fa file")
    parser_settings.add_argument("--suffix_fq", type = str,
                                 help = "the suffix of fq files. "
                                        "Don't include '.', good examples: [fastq, fq.gz]. [Default: {}]".format(defaults.defaults_settings["suffix_fq"]))
    parser_settings.add_argument("--dir_fq", type = str,
                                 help = "the dir containing fq files. "
                                        "Also make sure all fq files are like xx_R1/2.suffix")
    parser_settings.add_argument("--dir_bam", type = str,
                                 help = "the dir containing bam files. "
                                        "Note: each bam should be in a individual subfolder")

    ## ----- STAR ----- ##
    parser_star = newSubparser()
    parser_star.add_argument("-v", "--version", action = "version", version = version)
    parser_star.add_argument("--build_index", action = argparse.BooleanOptionalAction, default = None,
                             help = "build a star index or not")
    parser_star.add_argument("--dir_index", type = str, help = "star index directory")
    parser_star.add_argument("--name_star_dir", type = str,
                             help = "name of the output star dir. "
                                    "Can be set as 'star/subdir' to store outputs in a subfolder [Default: {}]".format(defaults.defaults_star["name_star_dir"]))
    parser_star.add_argument("--transcript_bam", action = argparse.BooleanOptionalAction, default = None,
                             help = "generate an additional transcript bam or not")
    parser_star.add_argument("--ram_bamsort", type = int, metavar = "50000000000, ...",
                             help = "an error maybe occur when sorting the bam. "
                                    "If so, set this parameter higher [Default: {}]".format(defaults.defaults_star["ram_bamsort"]))
    parser_star.add_argument("--soft_clip", action = argparse.BooleanOptionalAction, default = None,
                             help = "set '--no-soft_clip' will add '--alignEndsType EndToEnd' to STAR mapping command to suppress soft-clip")
    parser_star.add_argument("--phred", type = int, help = "phred33 is predominant "
                                                           "[Default: {}]".format(defaults.defaults_star["phred"]))

    ## ----- RSEM ----- ##
    parser_rsem = newSubparser()
    parser_rsem.add_argument("-v", "--version", action = "version", version = version)
    parser_rsem.add_argument("--fq", action = argparse.BooleanOptionalAction, default = None,
                             help = "run RSEM based on fq files and use bowtie2 as the aligner")
    parser_rsem.add_argument("--path_bowtie2", type = str, metavar = "~/bin/",
                             help = "path containing executable bowtie2. "
                                    "[Default: {}]".format(defaults.defaults_rsem["path_bowtie2"]))
    parser_rsem.add_argument("--prepare_reference", action = argparse.BooleanOptionalAction, default = None,
                             help = "prepare rsem reference or not")
    parser_rsem.add_argument("--prefix_reference", type = str, metavar = "~/doc/reference/rsem/index",
                             help = "rsem reference prefix")
    parser_rsem.add_argument("--name_rsem_dir", type = str,
                             help = "name of the output rsem dir. "
                                    "Can be set as 'rsem/subdir' to store outputs in a subfolder [Default: {}]".format(defaults.defaults_rsem["name_rsem_dir"]))

    ## ----- fastqc ----- ##
    parser_fastqc = newSubparser()
    parser_fastqc.add_argument("-v", "--version", action = "version", version = version)
    parser_fastqc.add_argument("--name_fastqc_dir", type = str,
                               help = "name of the output fastqc dir. "
                                      "Can be set as 'fastqc/subdir' to store outputs in a subfolder [Default: {}]".format(defaults.defaults_fastqc["name_fastqc_dir"]))

    ## ----- subcommands ----- ##
    subparsers = parser_top.add_subparsers(title = "different tools to tackle data",
                                           description = "supported tools so far are as follows",
                                           help = "select one to see details")

    parser_sub_star = subparsers.add_parser("star",
                                            help = "run STAR mapping or build an index",
                                            description = "===== STAR algorithm =====",
                                            epilog = "***** watch the STAR version *****",
                                            parents = [parser_groups, parser_star])
    parser_sub_star.set_defaults(func = star.star)

    parser_sub_rsem = subparsers.add_parser("rsem",
                                            help = "run RSEM quantification or prepare a reference",
                                            description = "===== RSEM algorithm =====",
                                            epilog = "***** watch the RSEM version *****",
                                            parents = [parser_groups, parser_rsem])
    parser_sub_rsem.set_defaults(func = rsem.rsem)

    parser_sub_rsem = subparsers.add_parser("fastqc",
                                            help = "quality control by FastQC",
                                            description = "===== fastqc algorithm =====",
                                            epilog = "***** watch the FastQC version *****",
                                            parents = [parser_groups, parser_fastqc])
    parser_sub_rsem.set_defaults(func = fastqc.fastqc)

    args = parser_top.parse_args()

    if len(sys.argv) == 1:
        args = parser_top.parse_args(["-h"])

    ##### common and paths settings classes #####
    common = Common.Common(args.print_class, args.index, args.yaml_file,
                           args.samples, args.dir_project, args.run, args.check)
    settings = Settings.Settings(args.nproc, args.gtf, args.fa, args.suffix_fq, args.dir_fq, args.dir_bam)

    common.loadSampleIds()
    common.loadYamlFile()

    ##### update settings and reload samples #####
    common.subSet(defaults.defaults_common)
    common.loadSampleIds()
    settings.subSet(common, defaults.defaults_settings)

    ##### call different functions according to sub commands #####
    args.func(args, common, settings)


if __name__ == "__main__":
    main()
