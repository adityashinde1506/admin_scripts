#!/usr/bin/env python3

import os
import sys

main_class=sys.argv[1]
arg=sys.argv[2:]

run_cmd="mvn exec:java -Dexec.mainClass=%s -Dexec.args=%s"
os.system(run_cmd%(main_class,",".join(arg)))
