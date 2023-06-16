#!/usr/bin/env python3
#
# Copyright 2023 Jeffrey M. Squyres.  All rights reserved.
#
# $COPYRIGHT$
#
# Additional copyrights may follow
#
# $HEADER$

# Trivial script to scrape section names from source .rst files and
# generate dummy show_help-style text files.  We only use this script
# a) if the show_help files are not availabale (i.e., in a git clone),
# and b) if Sphinx is not available.
#
# We generate these show_help files (as opposed to generating a run
# time error when the show_help file is unavailable) just so that it's
# 100% obvious that you're not getting proper help files because you
# did not have Sphinx available.

# Intentially use a minimal set of Python modules (to decrease any
# needed dependencies).

import re
import os
import sys

# Pop the executable name
exe = sys.argv.pop(0)
abs_srcdir = os.path.abspath(os.path.dirname(exe))

# First argument is the text outdir (in the build tree).
outdir = sys.argv.pop(0)
outdir_len = len(outdir) + 1

# The rest of the arguments are the text filenames to build.
for outfile in sys.argv:

    # The filenames all have the outdir prefix.  We find the
    # correspoding source .rst file by stripping that prefix off and
    # adding the srcdir prefix to it.
    #
    # We do this instead of using os.path.basename() because some
    # files have subdirectory names in them (e.g.,
    # "mca/help-something.txt").
    txt_filename = outfile[outdir_len:]

    # Replace the .txt with .rst, and add the srcdir prefix.
    rst_filename = txt_filename.replace(".txt", ".rst")
    srcfile = os.path.join(abs_srcdir, rst_filename)

    # Read in the source file
    with open(srcfile) as fp:
        src_rst = fp.readlines()

    # Find all the "[section]" lines.
    sections = list()
    for line in src_rst:
        match = re.search('\s*\[(.+)\]\s*$', line)
        if match:
            sections.append(match.group(1))

    # Ensure the out directory exists
    full_outdir = os.path.abspath(os.path.dirname(outfile))
    # Use older form of os.mkdirs (without the exist_ok param) to make
    # this script runnable in as many environments as possible.
    try:
        os.makedirs(full_outdir)
    except FileExistsError:
        pass

    # Write the output file
    with open(outfile, 'w') as fp:
        for section in sections:
            fp.write(f"""[{section}]
This help section is empty because PRRTE was built without Sphinx.\n""")
