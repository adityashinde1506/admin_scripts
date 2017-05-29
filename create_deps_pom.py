#!/usr/bin/env python3

import os
import sys

group=sys.argv[2]
version=sys.argv[3]
deps=os.listdir(sys.argv[1])

dep_string="<dependency><groupId>%s</groupId><artifactId>%s</artifactId><version>%s</version></dependency>"

for dep in deps:
    print(dep_string%(group,dep,version))
