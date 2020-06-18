#!/usr/bin/env python3
import subprocess
import os
import sys

#! https://askubuntu.com/a/796275

# --- set the list of valid extensions below (lowercase)
# --- use quotes, *don't* include the dot!
ext = ["jpg", "jpeg", "png", "svg", "icns", "ico"]
# ---

dr = sys.argv[1]

for root, dirs, files in os.walk(dr):
    for directory in dirs:
        folder = os.path.join(root, directory)
        try:
            first = min(p for p in os.listdir(folder) 
                        if p.split(".")[-1].lower() in ext)
        except ValueError:
            pass
        else:
              subprocess.Popen([
                  #"gvfs-set-attribute",
                  "gio", "set", "-t", "string",
                  os.path.abspath(folder), "metadata::custom-icon",
                  "file://"+os.path.abspath(os.path.join(folder, first))
                  ])
