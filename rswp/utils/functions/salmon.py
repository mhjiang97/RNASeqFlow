from ..classes.Salmon import *
from .. import defaults

def salmon(args, common, settings):
    mysalmon = Salmon(args.dir_index, args.name_salmon_dir, common, settings)
    mysalmon.subSet(defaults.defaults_salmon)
    mysalmon.generateCmds()
    addCmd(mysalmon, mysalmon.name, mysalmon.common.add)
    if mysalmon.settings.gtf is None:
        mysalmon - {"Salmon quantification": "--geneMap None"}
    mysalmon.runCmds()
