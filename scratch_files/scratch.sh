#!/bin/bash
if [ $# -eq 0 ]; then
  echo "No arguments provided."
fi
while getopts "a:b:c" opt; do
  case $opt in
    a)
      echo "Option -a was triggered with argument: $OPTARG"
      ;;
    b)
      echo "Option -b was triggered with argument: $OPTARG"
      ;;
    c)
      echo "Option -c was triggered (no argument required)"
      ;;
    *)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
