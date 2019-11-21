#######################################################
# Change version for each packages
#######################################################
# 1) go where is the multisetup.py
# 2) change lines 21-23 to adapt to the good version
# 3) launch what is here:

import os
from openalea.core.path import path

di = [d for d in path(".").listdir() if d.isdir()]
di.remove(".svn")

filename = "metainfo.ini"
for d in di:
    print d
    if (path(d)/filename).exists():
        f = (path(d)/filename).open("r+")
        text = f.read()
        text = text.replace("release = 0.9","release = 1.1")
        text = text.replace("version = 0.9.0","version = 1.1.0")
        text = text.replace("version = 0.9.1","version = 1.1.0")
        f.seek(0)
        f.write(text)
        f.close()
        print d, "ok", "1.1" in text
