# RSWP: RNA-seq Workflow by Python <img src="https://github.com/mhjiang97/RNASeqFlow/blob/master/rswp/utils/sticker/sticker.png" align="right" height=150 width=140/>  
## _A library for easy RNA-seq analysis_  
_(Note: only for paired-end data so far and upgrade your python to 3.9)_
  
-----------
## Author  
Minghao Jiang, <jiangminghao1001@163.com>  

## Table of Contents  
- [supported tools](#supported-tools)  
- [features](#features)  
- [license](#license)

## Supported tools  
**_make sure supported tools are executable in your PATH_**  

- `FastQC`
  
    > + quality control on fastq files  
    > + get more information via [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)  
    
- `STAR`  
  
    > + [STAR](https://github.com/alexdobin/STAR) mapping algorithm  
    > + both genome bam and transcriptome bam are supported  
    
- `RSEM`  
  
    > + [RSEM](https://github.com/deweylab/RSEM) quantification algorithm  
    > + based on existing bam or directly mapping fq files with bowtie2  
    
- `SAMtools`  
  
    > + [SAMtools](https://github.com/samtools/samtools) utilities for manipulating alignments  
    > + supported for only samtools index so far  
    
- `Salmon`
  
    > + [Salmon](https://github.com/COMBINE-lab/salmon) quantification algorithm
    > + mapping-based mode only  

- _Applications for other tools are being built..._  

## Features
  
### 1. Run one tool on a list of samples  
- Download the rswp package:
  
    ```bash
    git clone https://github.com/mhjiang97/RNASeqFlow.git
    cd RNASeqFlow
    ##### install required python modules #####
    pip install -r requirements.txt
    cd rswp
    ##### add dir RNASeqFlow/rswp/ to your PATH #####
    echo -e "\n# >>> rswp initialize >>>\nexport PATH=\${PATH}:`pwd`/\n# <<< rswp initialize <<<\n" >> ~/.bashrc
    ```  
- Get help first:
  
    ```bash
    rswp.py star -h
    ```  
- Run `STAR` with a file with sample ids:
    
    ```bash
    ##### build an index first #####
    rswp.py star --build_index --dir_index ${my_star_index} --gtf ${gtf_file} --fa ${fa_file}
    
    for i in {1..5}
    do
        rswp.py star --index ${i} --samples samples.txt --dir_index ${my_star_index} --dir_fq ${fq_dir} &
    done
    ```  
- Run `STAR` with samples available on the command line:
  
    ```bash
    for i in {1..5}
    do
        rswp.py star --index ${i} --samples M1 M2 M3 M4 M5 --dir_index ${my_star_index} --dir_fq ${fq_dir} &
    done
    ```  
- Or you can also call `STAR` like:
  
    ```bash
    for s in M1 M2 M3 M4 M5
    do
        rswp.py star --samples ${s} --dir_index ${my_star_index} --dir_fq ${fq_dir} &
    done
    ```
  
### 2. Run a workflow on a list of samples  
- First modify the run.sh at the bottom to encapsulate a workflow you prefer:
  
    ```shell
    ####################
    ### run.sh codes ###
    ### ...          ###
    ### at bottom:   ###
    ####################
    rswp.py star --samples "${sample}" --config "${config}" --dir_index ${my_star_index} --dir_fq ${my_fq_dir}
    rswp.py rsem --samples "${sample}" --config "${config}" --prefix_reference ${my_rsem_reference} --dir_bam ${my_bam_dir}
    ```  
- `run.sh` expects two arguments "-s" and "-c", which represent "sample" and "config" respectively:
  
    ```bash
    for s in M1 M2 M3 M4 M5
    do
        bash run.sh -s ${s} -c config.yaml &
    done
    ```  
- If you pass nothing to flag s, please give the run.sh two positional parameters:
  
    ```bash
    for i in {1..5}
    do
        bash run.sh -c config.yaml samples.txt ${i} &
    done
    ```  
  
### 3. Run workflow on cluster  
- A sample sbatch file is like:
  
    ```bash
    cat workflow.sbatch
    ```  
    ```shell
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
- Then submit it to the computing node:
  
    ```bash
    sbatch workflow.sbatch
    ```  
  
### 4. Config based  
- A config file must be in yaml format and have at least two hierarchies:
  
    ```yaml
    ###########################
    ### config.yaml contents ##
    ###########################
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
- Remember: command line parameters always take precedence over corresponding settings in the config:
  
    ```bash
    rswp.py star --samples M1 --config config.yaml --dir_index ~/doc/reference/mouse/star_2.7.5a  
    ```  
    the code above will run star mapping against `~/doc/reference/mouse/star_2.7.5a` instead of `~/doc/reference/star_2.7.5a`
  
### 5. Check commands  
- Add `--no-run` to rswp, and it will not call `subprocess.Popen()` but only print commands on the screen,
  so you can check if commands are what you want:
  
    ```bash
    rswp.py star --samples M1 --config config.yaml --no-run
    ```
  
### 6. Add or delete flags after checking  
- After running rswp.py with --no-run, you already manually check if the commands are what you desired.  
- If you're going to modify commands without editing source codes, use `--add` to give specific steps more arguments 
or use `--sub` to eliminate ones that didn't meet your requirements:  
  
    ```bash
    ### check commands
    rswp.py salmon --samples M1 --config config.yaml --no-run
    ### add some arguments
    rswp.py salmon --samples M1 --config config.yaml --add '{"Salmon":{"Salmon quantification":"--dumpEq --numBootstraps 100"}}'
    ```
  
## License  
RSWP is licensed under the [GNU General Public License v3](http://www.gnu.org/licenses/gpl-3.0.html)  
