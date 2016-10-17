# data toys

This is a set of gross scripts for messing with large amounts of RHEL content.

I wrote them in an afternoon. Don't judge them too harshly, they're just for
gathering some example data.

## `rsync.sh`

rsync some RHEL releases into a local directory.

The trees to grab are listed in `trees.txt`.

You'll need to mount `/vol/engarchive2` somewhere.

## `extractrpms.sh`

Usage: `extractrpms.sh RPMTREE OUTROOT`

Unpack all the RPMs in the directory RPMTREE into a new directory structure
under OUTROOT.

The directory structure looks like this, for each RPM:

    OUTROOT/${pkg:0:1}/$pkg/$evr/$arch/$name/ # package contents are here
    OUTROOT/by-rpm/${rpm:0:1}/$rpm            # symlink to above dir

(where `$pkg` is the _source_ RPM name, `$name` is the binary RPM package
(or subpackage) name, and `$rpm` is the name of the RPM file itself, e.g.:

    content: rpms/x/xz/5.1.2-8alpha.el7/x86_64/xz-libs/
    symlink: rpms/by-rpm/x/xz-libs-5.1.2-8alpha.el7.x86_64.rpm

**NOTE**: this de-duplicates RPMs that have the same ENVRA.

## `analyze_contents.sh` OUTROOT

Runs file(1) and sha256sum(1) on all the files in an OUTROOT from
`extractrpms.sh`.

Writes files named SHA256SUM.$OUTROOT and FILE.$OUTROOT.

Does really stupid parallelization - runs one process for each letter
under OUTROOT. Which means the 'x' one finishes quickly but the 'g' one
takes forever. Whatever.

## `unique-files.py`

Take a huge SHA256SUM file and prints only one line for each set of files that have
the same sha256sum.

# Notes / bugs / etc.

I probably should have written these tools in Python instead, but I was just
doing this as a Friday afternoon experiment so I wrote the quickest, dirtiest
things I could.

`extractrpms.sh` *could* be paralallelized.

# Test results so far

Using the 16 trees that are currently in `trees.txt`:

* Total size of all RPMS: 47G
  * `find rheltrees -type f -name "*.rpm" -print0 | du -ch --files0-from=- | tail -n1`

* Total size of uncompressed RPM contents, duplicate files removed: 44G
  * `./unique-files.py | cut -b67- | tr '\n' '\0' | du -ch --files0-from=- | tail -n1`

* Total size of xz-compressed, deduplicated RPM contents: 14G
  * `mksquashfs rpms rpms.sqfs -comp xz -always-use-fragments && du -h rpms.sqfs`
