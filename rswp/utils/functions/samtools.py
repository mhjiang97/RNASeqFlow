from ..classes.Samtools import *
from .. import defaults

def samtools(args, common, settings):
    mysamtools = Samtools(args.mode, common, settings)
    mysamtools.subSet(defaults.defaults_samtools)
    mysamtools.generateCmds()
    addCmd(mysamtools, mysamtools.name, mysamtools.common.add)
    mysamtools.runCmds()
