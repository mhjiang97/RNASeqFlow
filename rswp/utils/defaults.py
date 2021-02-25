##### set defaults #####
defaults_star = dict(zip(["build_index", "name_star_dir", "transcript_bam", "gene_counts", "ram_bamsort", "soft_clip", "phred"], [False, "star", False, False, 80000000000, True, 33]))
defaults_common = dict(zip(["print_class", "index", "dir_project", "run", "check"], [False, 1, "./", True, True]))
defaults_settings = dict(zip(["nproc", "suffix_fq", "suffix_bam"], [10, "fq.gz", "SortedByCoord.bam"]))
defaults_rsem = dict(zip(["fq", "path_bowtie2", "prepare_reference", "name_rsem_dir"], [False, "\'\'", False, "rsem"]))
defaults_fastqc = dict(zip(["name_fastqc_dir"], ["fastqc"]))
defaults_samtools = dict(zip(["mode"], ["index"]))
defaults_salmon = dict(zip(["name_salmon_dir"], ["salmon"]))