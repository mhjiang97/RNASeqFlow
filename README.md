# RSWP: RNA-seq Workflow by Python

<!-- markdownlint-disable MD033 -->
<img src="https://github.com/mhjiang97/RNASeqFlow/blob/master/src/rswp/sticker/sticker.png" alt="RSWP sticker" align="right" height=100 width=100/>

A library for easy RNA-seq analysis

> **Note:** Currently supports only paired-end data. Requires Python 3.9 or higher.

## Author

Minghao Jiang, <jiangminghao1001@163.com>

## Table of Contents

- [RSWP: RNA-seq Workflow by Python](#rswp-rna-seq-workflow-by-python)
  - [Author](#author)
  - [Table of Contents](#table-of-contents)
  - [Supported Tools](#supported-tools)
  - [Installation](#installation)
  - [Usage Guide](#usage-guide)
    - [1. Running a Single Tool](#1-running-a-single-tool)
    - [2. Running a Full Workflow](#2-running-a-full-workflow)
    - [3. Running on a Cluster (SLURM)](#3-running-on-a-cluster-slurm)
    - [4. Using Configuration Files](#4-using-configuration-files)
    - [5. Dry Run (Checking Commands)](#5-dry-run-checking-commands)
    - [6. Modifying Commands on the Fly](#6-modifying-commands-on-the-fly)
  - [License](#license)

---

## Supported Tools

Ensure the following tools are installed and available in your system's `PATH`:

- **[FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)**: Quality control for FASTQ files.
- **[STAR](https://github.com/alexdobin/STAR)**: RNA-seq mapping algorithm (supports both genome and transcriptome BAMs).
- **[RSEM](https://github.com/deweylab/RSEM)**: Transcript quantification (can use existing BAMs or map directly with Bowtie2).
- **[SAMtools](https://github.com/samtools/samtools)**: Utilities for manipulating alignments (currently supports `samtools index`).
- **[Salmon](https://github.com/COMBINE-lab/salmon)**: Transcript quantification (mapping-based mode only).

_Support for additional tools is currently in development._

---

## Installation

Clone the repository and install the package using `uv`:

```bash
git clone https://github.com/mhjiang97/RNASeqFlow.git
cd RNASeqFlow

# Install the package in editable mode using uv
uv pip install -e .
```

Verify the installation by checking the help menu:

```bash
rswp -h
```

---

## Usage Guide

### 1. Running a Single Tool

You can run individual tools on one or multiple samples.

First, build the STAR index:

```bash
rswp star --build_index --dir_index /path/to/star_index --gtf /path/to/annotation.gtf --fa /path/to/genome.fa
```

Then, run STAR on your samples. You can provide samples in several ways:

- **Using a file containing sample IDs:**

  ```bash
  for i in {1..5}; do
      rswp star --index ${i} --samples samples.txt --dir_index /path/to/star_index --dir_fq /path/to/fastq_dir &
  done
  ```

- **Passing sample IDs directly via command line:**

  ```bash
  for i in {1..5}; do
      rswp star --index ${i} --samples M1 M2 M3 M4 M5 --dir_index /path/to/star_index --dir_fq /path/to/fastq_dir &
  done
  ```

- **Iterating over sample IDs:**

  ```bash
  for s in M1 M2 M3 M4 M5; do
      rswp star --samples ${s} --dir_index /path/to/star_index --dir_fq /path/to/fastq_dir &
  done
  ```

### 2. Running a Full Workflow

You can encapsulate multiple steps into a shell script (`run.sh`).

Modify the bottom of `run.sh` to define your workflow:

```bash
####################
### run.sh codes ###
####################
rswp star --samples "${sample}" --config "${config}" --dir_index /path/to/star_index --dir_fq /path/to/fastq_dir
rswp rsem --samples "${sample}" --config "${config}" --prefix_reference /path/to/rsem_ref --dir_bam /path/to/bam_dir
```

Run the workflow using the `-s` (sample) and `-c` (config) flags:

```bash
for s in M1 M2 M3 M4 M5; do
    bash run.sh -s ${s} -c config.yaml &
done
```

Alternatively, pass the sample list file and an index:

```bash
for i in {1..5}; do
    bash run.sh -c config.yaml samples.txt ${i} &
done
```

### 3. Running on a Cluster (SLURM)

You can easily submit your workflow to a SLURM cluster using an array job.

Create a `workflow.sbatch` file:

```bash
#!/bin/bash
#SBATCH -p cpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --exclusive
#SBATCH --mail-type=end
#SBATCH --output=logs/slurm/workflow.%a.out
#SBATCH --error=logs/slurm/workflow.%a.err
#SBATCH --mail-user=jiangminghao1001@163.com
#SBATCH --array=1-5

bash run.sh -c config.yaml samples.txt ${SLURM_ARRAY_TASK_ID}
```

Submit the job:

```bash
sbatch workflow.sbatch
```

### 4. Using Configuration Files

RSWP uses YAML configuration files to manage settings. The file must have at least two hierarchies.

**Example `config.yaml`:**

```yaml
Common:
    dir_project: &dir_project ~/projects/AS/data/paper/
    print_class: False
STAR:
    dir_index: ~/doc/reference/star_2.7.5a
    name_star_dir: &name_star_dir star
Settings:
    gtf: ~/doc/reference/gtf/gencode.v32.annotation.gtf
    fa: ~/doc/reference/fa/GRCh38.p13.genome.fa
    dir_fq: ~/projects/AS/data/paper/
    dir_bam:
        - *dir_project
        - *name_star_dir
RSEM:
    prefix_reference: ~/doc/reference/rsem/index
```

> **Important:** Command-line arguments always override settings in the configuration file.
>
> ```bash
> rswp star --samples M1 --config config.yaml --dir_index ~/doc/reference/mouse/star_2.7.5a
> ```
>
> This will use `~/doc/reference/mouse/star_2.7.5a` instead of the path defined in `config.yaml`.

### 5. Dry Run (Checking Commands)

To preview the commands that will be executed without actually running them, use the `--no-run` flag:

```bash
rswp star --samples M1 --config config.yaml --no-run
```

### 6. Modifying Commands on the Fly

If you need to add or remove specific arguments from the generated commands without editing the source code, you can use the `--add` and `--sub` flags.

```bash
# 1. Check the default commands
rswp salmon --samples M1 --config config.yaml --no-run

# 2. Add custom arguments to the Salmon quantification step
rswp salmon --samples M1 --config config.yaml --add '{"Salmon":{"Salmon quantification":"--dumpEq --numBootstraps 100"}}'
```

---

## License

RSWP is licensed under the [GNU General Public License v3](http://www.gnu.org/licenses/gpl-3.0.html).
