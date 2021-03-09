#!/usr/bin/env bash
helpDoc(){
    cat <<EOF
Description:
    Encapsulate flows in a shell script

Usage:
    bash run.sh -s M5 -c config.yaml

Option:
    -s: sample to run
    -c: yaml config file passed to rswp

    if you don't pass a value to the parameter s then give run.sh a file incorporating ids with an index, like:
        bash run.sh -c config.yaml samples.txt 1

EOF
}

if [ $# -eq 0 ]
then
  helpDoc
  exit 1
fi

while getopts 's:c:h' OPT
do
  case $OPT in
    s)
      sample=${OPTARG}
      ;;
    c)
      config=${OPTARG}
      ;;
    h)
      helpDoc
      exit 1
      ;;
    ?)
      echo -e "Error: parameter unknown\n"
      helpDoc
      exit 1
      ;;
  esac
done
shift $((--OPTIND))
file=$1
index=$2
if [ "${sample}" = "" ]
then
  sample=$(gsed -n "${index}p" "${file}")
fi

# echo "${sample}"
# echo "${config}"
python rswp.py star -s "${sample}" -c "${config}" --no-run
python rswp.py rsem -s "${sample}" -c "${config}" --no-run

