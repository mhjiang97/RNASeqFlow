from ..classes.Rsem import *
from .. import defaults

def rsem(args, common, settings):
    ##### create an Rsem instance #####
    myrsem = Rsem(args.prepare_reference, args.prefix_reference, args.name_rsem_dir, common, settings)
    myrsem.subSet(defaults.defaults_rsem)
    myrsem.generateCmds()
    myrsem.runCmds()