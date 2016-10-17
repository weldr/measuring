#!/bin/bash

analyze_dir() {
    rm -f "$1/.FILE" "$1/.SHA256SUM"
    find "$1" -type f | while read f; do
        file "$f" >> "$1/.FILE"
        sha256sum "$f" >> "$1/.SHA256SUM"
    done
}

INROOT="$1"
[ -d "$INROOT" ] || \
    { echo "usage: analyze_contents.sh EXTRACTED_RPMS_DIR"; exit 1; }

subdirs=$(echo $INROOT/?)

for d in $subdirs; do
    [ -d "$d" ] || continue
    analyze_dir "$d" &
done
wait

cat $INROOT/?/.FILE > FILE.$INROOT
cat $INROOT/?/.SHA256SUM > SHA256SUM.$INROOT
rm $INROOT/?/.FILE $INROOT/?/.SHA256SUM
