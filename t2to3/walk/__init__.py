# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

import os
import subprocess

def walk(src, dst):
    """
    Walk through the src directory and generate 2to3 results to the associated files
    with same filename and folder organizations as the original source files in src.
    """
    # remove duplicated slash when dst replaced with the original file path
    if dst == './':
        dst = '.' 


    for root, dirs, fns in os.walk(src):
        for fn in fns:
            if fn.endswith(".py"):
                unprocess_fn = os.path.join(root, fn)
                output_dir = root.replace(src, dst)
                processed_fn = os.path.join(output_dir, fn)
                #TODO: change to logger.
                print("Processing...", unprocess_fn)

                # create the basedir of the output file
                if not os.path.isdir(output_dir):
                    os.makedirs(output_dir)
                p = subprocess.Popen(["2to3", unprocess_fn], stdout=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if stderr is not None:
                    with open(processed_fn + '.err', 'wb') as errfw:
                        errfw.write(stderr)
                if len(stdout) > 0:
                    with open(processed_fn + '.2to3', 'wb') as fw:
                        fw.write(stdout)
    
        for d in dirs:
            walk(d, dst)