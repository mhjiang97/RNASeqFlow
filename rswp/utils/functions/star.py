from ..classes.Star import *
from .. import defaults

def star(args, common, settings):
    if args.transcript_bam is None:
        tb = defaults.defaults_star["transcript_bam"]
        try:
            tb = common.returnSubSettings("STAR")["transcript_bam"]
        except KeyError:
            pass

    if tb:
        mystar = StarTransBam(args.build_index, args.dir_index, args.name_star_dir,
                              args.transcript_bam, args.ram_bamsort, args.soft_clip,
                              args.phred, common, settings)
    else:
        mystar = Star(args.build_index, args.dir_index, args.name_star_dir,
                      args.transcript_bam, args.ram_bamsort, args.soft_clip,
                      args.phred, common, settings)
    mystar.subSet(defaults.defaults_star)
    mystar.generateCmds()

    if not mystar.soft_clip:
        mystar + dict(zip(["STAR mapping"], ["--alignEndsType EndToEnd"]))

    mystar.runCmds()