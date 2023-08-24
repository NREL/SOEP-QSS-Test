#!/usr/bin/env python
# FMU Build Script Wrapper: Use GCC Compiler
import subprocess, sys
args = ' --gcc ' + ' '.join( sys.argv[1:] )
subprocess.run( 'bld_fmu.py' + args, shell = True )
