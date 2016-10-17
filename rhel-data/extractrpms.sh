#!/bin/bash

function extractrpm() {
    local rpm="$1" outroot="$2"
    local name epoch ver rel arch srpm pkg evr

    # read RPM headers into local vars
    eval $(rpm -qp "$rpm" --qf "
        name='%{NAME}'
        epoch='%{EPOCH}'
        ver='%{VERSION}'
        rel='%{RELEASE}'
        arch='%{ARCH}'
        srpm='%{SOURCERPM}'" 2>/dev/null)

    # parse the source package name from the SRPM filename
    pkg="${srpm%%-${ver}-${rel}*}" # source package name

    # fix up the epoch to give a proper EVR
    case "$epoch" in
        '(none)'|0) evr="${ver}-${rel}" ;;
        *) evr="${epoch}:${ver}-${rel}" ;;
    esac

    # construct the output dir name
    outdir="${pkg:0:1}/$pkg/$evr/$arch/$name/"

    # extract RPM payload into outdir
    mkdir -p "$outroot/$outdir"
    if rpm2cpio "$rpm" | ( cd "$outroot/$outdir" && cpio -iumd --quiet ); then
        echo "$outdir"
        return 0
    else
        rm -rf "$outroot/$outdir"
        return 1
    fi
}

# main program!

INROOT="$1"
OUTROOT="$2"
[ -d "$INROOT" ] && [ -n "$OUTROOT" ] && mkdir -p "$OUTROOT" \
    || { echo "usage: extractrpms.sh DIR_WITH_RPMS OUTPUT_DIR"; exit 1; }

find "$1" -type f -name "*.rpm" | while read f; do
    rpmfile="${f##*/}"
    symlinkdir="$OUTROOT/by-rpm/${rpmfile:0:1}"
    symlinkfile="$symlinkdir/$rpmfile"
    if [ -d "$symlinkdir" -a -d "$symlinkfile" ]; then
        echo "$rpmfile [skipped]"
    else
        if outdir=$(extractrpm "$f" "$OUTROOT"); then
            mkdir -p "$symlinkdir"
            ln -sf "../../$outdir" "$symlinkfile"
        fi
    fi
done
