#!/usr/bin/env python3
import subprocess
import os
import sys

#! https://askubuntu.com/a/796275

dr = sys.argv[1]

for root, dirs, files in os.walk(dr):
    for directory in dirs:
        folder = os.path.join(root, directory)
        subprocess.Popen([
            "gvfs-set-attribute", os.path.abspath(folder),
            "-t", "unset", "metadata::custom-icon"
            ])
