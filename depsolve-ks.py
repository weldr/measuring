#!/usr/bin/python3
#
# Output the package set that would be installed if the packages on the cmdline were installed
#

import os
import sys
import dnf
import argparse
import tempfile

from pykickstart.errors import KickstartError
from pykickstart.parser import KickstartParser
from pykickstart.version import DEVEL, makeVersion

def setup_argparse():
    parser = argparse.ArgumentParser(description="Output packages DNF has selected")

    # required arguments for image creation
    required = parser.add_argument_group("required arguments")
    required.add_argument("-r", "--release", help="release information", required=True, metavar="STRING")
    required.add_argument("-k", "--kickstart", help="kickstart file", required=True, metavar="STRING")
    parser.add_argument("--skip-broken", help="Skip broken packages. This is the DNF default.",
                        action="store_true", default=False)
    parser.add_argument("--tempdir", help="Directory to store temporary DNF files")

    return parser


def get_dbo(tempdir, repositories, releasever, best):
    """ Create a dnf Base object and setup the repositories and installroot

        :param list repositories: List of repositories to use for the installation
        :param string releasever: Release version to pass to dnf

    """
    def sanitize_repo(repo):
        """Convert bare paths to file:/// URIs, and silently reject protocols unhandled by yum"""
        if repo.startswith("/"):
            return "file://{0}".format(repo)
        elif any(repo.startswith(p) for p in ('http://', 'https://', 'ftp://', 'file://')):
            return repo
        else:
            return None

    # sanitize the repositories
    repositories = list(sanitize_repo(r) for r in repositories)

    # remove invalid repositories
    repositories = list(r for r in repositories if r)

    cachedir = os.path.join(tempdir, "dnf.cache")
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)

    logdir = os.path.join(tempdir, "dnf.logs")
    if not os.path.isdir(logdir):
        os.mkdir(logdir)

    installroot = os.path.join(tempdir, "installroot")
    if not os.path.isdir(installroot):
        os.mkdir(installroot)

    dnfbase = dnf.Base()
    conf = dnfbase.conf

    print("Use highest NVR package: %s" % best)
    conf.best = best

    # setup dirs.
    conf.logdir = logdir
    conf.cachedir = cachedir

    # Turn off logging to the console
    conf.debuglevel = 10
    conf.errorlevel = 0
    conf.debug_solver = True

    conf.releasever = releasever
    conf.installroot = installroot
    conf.prepend_installroot('persistdir')
    conf.tsflags.append('nodocs')

    # add the repositories
    for i, r in enumerate(repositories):
        if "SRPM" in r or "srpm" in r:
            print("Skipping source repo: %s" % r)
            continue
        repo_name = "lorax-repo-%d" % i
        repo = dnf.repo.Repo(repo_name, cachedir)
        repo.baseurl = [r]
        repo.skip_if_unavailable = False
        repo.enable()
        dnfbase.repos.add(repo)
        print("Added '%s': %s" % (repo_name, r))
        print("Fetching metadata...")
        try:
            repo.load()
        except dnf.exceptions.RepoError as e:
            print("Error fetching metadata for %s: %s" % (repo_name, e))
            return None

    dnfbase.fill_sack(load_system_repo=False)
    dnfbase.read_comps()

    return dnfbase


if __name__ == "__main__":
    parser = setup_argparse()
    opts = parser.parse_args()

    # Grab and parse the kickstart file.
    try:
        handler = makeVersion(DEVEL)
        ksparser = KickstartParser(handler)
        ksparser.readKickstart(opts.kickstart)
    except KickstartError as err:
        print("Failed to process kickstart file: %s\n" % err)
        sys.exit(1)

    # FIXME:  Handle groups and environments
    packages = ksparser.handler.packages.packageList

    # FIXME: Does this need to handle mirrorlists?  get_dbo sure doesn't.
    repos = map(lambda r: r.baseurl, ksparser.handler.repo.repoList)

    if len(packages) == 0:
        print("No packages given in the kickstart file!")
        sys.exit(1)

    tempdir = opts.tempdir or tempfile.mkdtemp(prefix="test-dnf.")
    print("Using tempdir: %s" % tempdir)
    dbo = get_dbo(tempdir, repos, opts.release, not opts.skip_broken)

    # Print all the packages DNF picks
    for pkg in packages:
        print("Adding %s to the transaction" % pkg)
        try:
            dbo.install(pkg)
        except Exception as e:
            print("Failed to install %s\n%s" % (pkg, e))

    try:
        print("Checking dependencies")
        dbo.resolve()
    except dnf.exceptions.DepsolveError as e:
        print("Dependency check failed: %s" % e)
        raise
    print("%d packages selected" % len(dbo.transaction))
    if len(dbo.transaction) == 0:
        raise Exception("No packages in transaction")

    # Print what DNF picked.
    for pkg in dbo.transaction.install_set:
        print("%s-%s-%s.%s.rpm" % (pkg.name, pkg.version, pkg.release, pkg.arch))
