#!/bin/bash

MOUNTPOINT="/mnt/engarchive2"
RHEL7DIR="$MOUNTPOINT/released/RHEL-7"

if [ ! -d "$RHEL7DIR" ]; then
    echo "error: mount engarchive2 at ${MOUNTPOINT}."
    exit 1
fi

TREES="$(for t in $(< trees.txt); do echo $t/os; done)"

(
    TARGET=$PWD/trees
    cd $RHEL7DIR
    rsync -azRP --chown=$(id -un):$(id -gn) $TREES "$TARGET/"
)
