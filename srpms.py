#!/usr/bin/python3
#
# Print a sorted list of all SRPMs.
# This works against the repos configured on the system.  So if you've got
# RHEL7 installed, it will tell you about RHEL7.  If you've got rawhide, it'll
# tell you about that.

import dnf

base = dnf.base.Base()
base.read_all_repos()
base.fill_sack()

q = base.sack.query().available()

srpms = {}

for pkg in list(q):
    if pkg.sourcerpm in srpms:
        srpms[pkg.sourcerpm].append(pkg.name)
    else:
        srpms[pkg.sourcerpm] = [pkg.name]

for (key, val) in sorted(srpms.items()):
    print("%s = %s %s" % (key, len(val), val))
