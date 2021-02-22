from ..classes.Fastqc import *
from .. import defaults

def fastqc(args, common, settings):
    myfastqc = Fastqc(args.name_fastqc_dir, common, settings)
    myfastqc.subSet(defaults.defaults_fastqc)
    myfastqc.generateCmds()
    addCmd(myfastqc, myfastqc.name, myfastqc.common.add)
    myfastqc.runCmds()
