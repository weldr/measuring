#!/usr/bin/python

import os

# TODO: this could totally be constructed from a simple data file:
# [ELF]
# matchwords = ["ELF"]
# [video]
# matchwords = ["video", "WebM"]
# [locale]
# basename = "locale-archive.tmpl"

def simplify_type(f, t):
    '''Simplify the output from file(1) to a simple category'''
    # Fix up things that just say "data"
    if t == "data":
        if f.endswith("locale-archive.tmpl"):
            t = "locale archive"
        elif f.endswith("classes.jsa"):
            t = "Java Shared Archive"
        elif f.endswith(".ja") or f.endswith(".jar"):
            t = "JAR file"
        elif 'firmware' in f:
            t = "firmware"
        elif 'libreoffice' in f or 'openoffice' in f:
            t = 'openoffice'
        else:
            t = "[unknown]"
    # Simplify long, complicated types
    if t.startswith('ELF') or ' ELF ' in t:
        return 'ELF'
    elif 'text' in t:
        return 'text'
    elif 'message catalog' in t or 'locale archive' in t:
        return 'locale/.mo'
    elif 'gzip' in t:
        return 'gzip'
    elif 'Java' in t:
        return 'java'
    elif 'image' in t:
        return 'image'
    elif 'video' in t or "WebM" in t:
        return 'video'
    elif 'audio' in t:
        return 'audio'
    elif 'GIMP' in t:
        return 'GIMP'
    elif t.startswith('dBase'):
        return 'dBase'
    elif 'ar archive' in t:
        return 'ar archive'
    elif 'python' in t:
        return 'python'
    elif t.startswith('Zip'):
        return 'zip'
    elif t.startswith('bzip2'):
        return 'bzip2'
    elif t.startswith('XZ'):
        return 'xz'
    elif t.startswith('timezone data'):
        return 'timezone data'
    elif 'SQLite' in t:
        return 'sqlite'
    elif "Berkeley DB" in t:
        return "Berkeley DB"
    elif "PDF" in t:
        return "pdf"
    elif "Emacs" in t:
        return "emacs"
    elif ('font data' in t or 'font metric' in t or 'PFM data' in t or
            'TrueType' in t or 'Open Font' in t or 'Font data' in t or
            "font program data" in t):
        return 'font'
    elif 'G-IR binary database' in t:
        return 'G-IR'
    elif 'GVariant Database' in t:
        return 'GVariant Database'
    elif t.startswith('Linux '):
        return 'Linux kernel'
    elif "SE Linux policy" in t:
        return "SELinux policy"
    elif 'EFI' in t:
        return 'EFI binary'
    elif ('PE32' in t or 'PE64' in t) and 'executable' in t:
        return 'Windows .exe'
    else:
        return t

def main(infile):
    print("Reading {}...".format(infile))
    files = dict(line.strip().split(': ',1) for line in open(infile))

    print("Getting file sizes...")
    # TODO: cache this data once generated
    sizes = {f:os.stat(f).st_size for f in files}
    total = sum(sizes.values())
    print("Total size: {:.1f}GB".format(total / 2**30))

    files_by_type = dict()
    for f in files:
        t = simplify_type(f, files[f])
        files_by_type.setdefault(t,[]).append(f)
    del files

    size_by_type = [(t,sum(sizes[f] for f in files_by_type[t]))
                    for t in files_by_type]

    data_files = [(f,sizes[f]) for f in files_by_type['[unknown]']]
    print("Unidentified files:")
    for f,s in sorted(data_files, key=lambda a: a[1]):
        print("{} {}".format(s, f))

    print("Data by type:")
    misc = 0
    for t, s in sorted(size_by_type, key=lambda a: a[1]):
        pct = 100.0 * s / total
        if pct < 0.1:
            misc += s
        elif misc:
            mpct = 100.0 * misc / total
            print("{:4.1f}%: Miscellaneous".format(mpct))
            misc = None
        print("{:4.1f}%: {}".format(pct, t))

if __name__ == '__main__':
    import sys
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        raise SystemExit(2)
