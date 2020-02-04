# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

import os
import subprocess
import sys
# sys.setrecursionlimit(100000)

class Walker:
    def __init__(self):
        self.unprocessed_pairs= []

    def check(self, src, dst):
        """
        Walk through the src directory and generate 2to3 results to the associated files
        with same filename and folder organizations as the original source files in src.
        """
        # remove duplicated slash when dst replaced with the original file path
        if dst == './':
            dst = '.' 

        for root, dirs, fns in os.walk(src, topdown=True):
            for fn in fns:
                if fn.endswith(".py"):
                    unprocess_fn = os.path.join(root, fn)
                    output_dir = root.replace(src, dst)
                    processed_fn = os.path.join(output_dir, fn)

                    self.unprocessed_pairs.append({unprocess_fn:processed_fn})
                    #TODO: change to logger.
                    print("Added...", unprocess_fn)
        
        for item in self.unprocessed_pairs:
            self._check_and_output(item)

    def _check_and_output(self, unprocessed_pair):
        for unprocess_fn, processed_fn in unprocessed_pair.items():
            output_dir = os.path.dirname(processed_fn)
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

    def scan(self, src):
        for root, dirs, fns in os.walk(src, topdown=True):
            for fn in fns:
                print(os.path.join(root, fn))