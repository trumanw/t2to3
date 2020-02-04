# t2to3

A command-line interface to run the python 2to3 on a Python project. 

# Installation
## From Source Code
Download the latest commit of the master branch and run the script below under the root directory:
```
python setup.py install
```

# Command-line Interface
## Project Validation
```
t2to3 check src_project dst_project
```

It will automatically scan the files and folders under the `src_project` and output as the same relative directories organization to `dst_project` folder.

The output file types:
t2to3.out: it contains all the runtime logs.
t2to3.err: it contains all the errors.
*.2to3: the results of the 2to3 mapped to the original source file by filename.

# Features
- Ignore folders listed in the input project's .gitignore file.
- Tracing progress with tqdm
- Versioneer