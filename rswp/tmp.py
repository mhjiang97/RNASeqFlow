import re, sys, os, argparse
def main():
    myparser = argparse.ArgumentParser(description = "generate a tx2gene file")
    myparser.add_argument("-i", "--input", type = str, help = "input a gtf file")
    myparser.add_argument("-o", "--output", type = str, help = "a file to output")
    args = myparser.parse_args()

    tx_file = os.path.expanduser(args.input)
    gene = re.compile("gene_id \"(.*?)\";")
    iso = re.compile("transcript_id \"(.*?)\";")
    tx_to_gene = {}
    name = re.compile("gene_name \"(.*?)\";")
    tx_to_name = {}
    gene_to_chr = {}
    with open(tx_file, 'r') as fh:
        for line in fh:
            if line[0] == '#':
                continue
            fields = line.strip().split("\t")
            if fields[2] == "gene":
                continue
            gret = gene.search(fields[8])
            tret = iso.search(fields[8])
            nret = name.search(fields[8])
            chromosome = fields[0]
            if not gret:
                g = "NA"
            else:
                g = gret.group(1)
            if not tret:
                t = "NA"
            else:
                t = tret.group(1)
            if not nret:
                n = "NA"
            else:
                n = nret.group(1)
            if t not in tx_to_gene:
                tx_to_gene[t] = g
            if t not in tx_to_name:
                tx_to_name[t] = n
            if g not in gene_to_chr:
                gene_to_chr[g] = chromosome

    fh.close()

    new_file = open(os.path.expanduser(args.output), "w")
    for key in tx_to_gene:
        g = tx_to_gene[key]
        chromosome = gene_to_chr[g]
        g_name = tx_to_name[key]
        line_new = "\t".join([chromosome, g, g_name, key]) + "\n"
        new_file.write(line_new)

    new_file.close()

if __name__ == "__main__":
    main()