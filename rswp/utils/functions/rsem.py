from ..classes.Rsem import *
from .. import defaults


def rsem(args, common, settings):
    if args.fq is None:
        fq = defaults.defaults_rsem["fq"]
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
    myrsem.subSet(defaults.defaults_rsem)
    myrsem.generateCmds()
    addCmd(myrsem, myrsem.name, myrsem.common.add)
    minusCmd(myrsem, myrsem.name, myrsem.common.sub)
    myrsem.runCmds()
