from ..classes.Star import *
from .. import defaults

def star(args, common, settings):
    if args.transcript_bam is None:
        tb = defaults.defaults_star["transcript_bam"]
        try:
            tb = common.returnSubSettings("STAR")["transcript_bam"]
        except KeyError:
            pass
    else:
        tb = args.transcript_bam
    print(tb)
    if tb:
        mystar = StarTransBam(args.build_index, args.dir_index, args.name_star_dir,
                              args.transcript_bam, args.gene_counts, args.ram_bamsort,
                              args.soft_clip, args.phred, common, settings)
    else:
        mystar = Star(args.build_index, args.dir_index, args.name_star_dir,
                      args.transcript_bam, args.gene_counts, args.ram_bamsort,
                      args.soft_clip, args.phred, common, settings)
    mystar.subSet(defaults.defaults_star)
    mystar.generateCmds()
    if mystar.gene_counts:
        if tb:
            mystar - dict(zip(["STAR mapping"], ["--quantMode TranscriptomeSAM"]))
            mystar + dict(zip(["STAR mapping"], ["--quantMode TranscriptomeSAM GeneCounts"]))
        else:
            mystar + dict(zip(["STAR mapping"], ["--quantMode GeneCounts"]))
    if not mystar.soft_clip:
        mystar + dict(zip(["STAR mapping"], ["--alignEndsType EndToEnd"]))
    addCmd(mystar, mystar.name, mystar.common.add)
    mystar.runCmds()
