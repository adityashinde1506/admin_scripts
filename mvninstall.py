#!/usr/bin/env python3

import os
import sys

_dir=sys.argv[1]
group=sys.argv[2]
jarfiles=os.listdir(_dir)
for jar in jarfiles:
    install_cmd="mvn install:install-file -Dfile=%s -DgroupId=%s -DartifactId=%s -Dpackaging=jar -Dversion=1.0"%(_dir+jar,group,jar.rsplit(".")[0])
    #print(install_cmd)
    os.system(install_cmd)
