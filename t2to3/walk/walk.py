# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

import os
import subprocess
import sys

class Walker:
    def __init__(self):
        self.unprocessed_pairs = []
        self.passed_files = []
        self.errlog = 't2to3.err'
        self.outlog = 't2to3.out'
        self.basedir = ''
        self.ignore_rules = []

    def check(self, src, dst, is_gitignore_enabled=True):
        """
        Walk through the src directory and generate 2to3 results to the associated files
        with same filename and folder organizations as the original source files in src.

        Args:
        - src: the source folder of the project needs to be checked.
        - dst: the output folder for keeping all the .2to3 result files.
        - is_gitignore_enabled: If it is True, read the .gitignore file from the root directory of src and ignore all the files/folders listed in it.
        """
        # load ignore file if is_gitignore_enabled
        if is_gitignore_enabled:
            if os.path.isfile(os.path.join(src, '.gitignore')):
                ignore_file_lines = open(os.path.join(src, '.gitignore')).readlines()
                for l in ignore_file_lines:
                    if not l.strip().startswith('#') and l.strip() != '' and l.strip()[-1] == '/':
                        self.ignore_rules.append(l.strip())

        # remove duplicated slash when dst replaced with the original file path
        if dst == './':
            dst = '.'
        self.basedir = dst
        # create the dst directory
        if not os.path.isdir(dst):
            os.makedirs(dst)

        self.errlog = os.path.join(self.basedir, self.errlog)
        self.outlog = os.path.join(self.basedir, self.outlog)

        #TODO: change to logger
        print("\nScanning project...\n")
        for root, dirs, fns in os.walk(src, topdown=True):
            for fn in fns:
                if fn.endswith(".py"):
                    unprocess_fn = os.path.join(root, fn)
                    output_dir = root.replace(src, dst, 1)  # only need to replace the first one
                    processed_fn = os.path.join(output_dir, fn[:-2] + '2to3')   # .2to3 is the file ext.
                    if not self._check_ignore(src, unprocess_fn):
                        self.unprocessed_pairs.append({unprocess_fn:processed_fn})

                        #TODO: change to logger.
                        with open(self.outlog, 'a') as outfw:
                            outfw.write("File added: {}.\n".format(unprocess_fn))
                    else:
                        with open(self.outlog, 'a') as outfw:
                            outfw.write("File ignored: {}.\n".format(unprocess_fn))

        from tqdm import trange

        #TODO: change to logger.
        print("\nStart analyzing {} python files...\n".format(len(self.unprocessed_pairs)))
        interval = 0.1
        total = len(self.unprocessed_pairs)
        text = "est. {:<04.2}s".format(interval * total)
        t = trange(total, desc=text)
        for i in t:
            self._check_and_output(self.unprocessed_pairs[i])

        #TODO: change to logger.
        print("\nStart removing {} empty analysis result files...\n".format(len(self.passed_files)))
        interval = 0.05
        total = len(self.passed_files)
        text = "est. {:<04.2}s".format(interval * total)
        t = trange(total, desc=text)
        for i in t:
            self._delete_empty_file(self.passed_files[i])

    def _check_and_output(self, unprocessed_pair):
        for unprocess_fn, processed_fn in unprocessed_pair.items():
            output_dir = os.path.dirname(processed_fn)
            # create the basedir of the output file
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)

            with open(processed_fn, 'wb') as outfw, open(self.errlog, 'a') as errfw:
                p = subprocess.Popen(["2to3", unprocess_fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                pstdout, pstderr = p.communicate()
                if pstdout is not None and pstdout != '':
                    outfw.write(pstdout)
                else:
                    self.passed_files.append(processed_fn)

                if pstderr is not None:
                    errfw.write(pstderr)
    
    def _delete_empty_file(self, empty_file):
        with open(self.outlog, 'a') as outfw:
            os.remove(empty_file)
            outfw.write("Empty file deleted: {}.\n".format(empty_file))
    
    def _check_ignore(self, src, fn):
        prefix_path = src
        if src[-1] != '/':
            prefix_path = src + '/'
        if not os.path.isdir(prefix_path):
            return False
        
        relative_fn_path = fn.replace(prefix_path, '', 1)
        if len(self.ignore_rules) > 0:
            ign_val = False
            for ign_dir in self.ignore_rules:
                if relative_fn_path.startswith(ign_dir):
                    ign_val = True
            return ign_val
        else:
            return False

    def scan(self, src):
        for root, dirs, fns in os.walk(src, topdown=True):
            for fn in fns:
                print(os.path.join(root, fn))