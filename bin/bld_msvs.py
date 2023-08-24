#!/usr/bin/env python
# FMU Build Script Wrapper: Use Microsoft Visual C++ Compiler
import subprocess, sys
args = ' --msvs ' + ' '.join( sys.argv[1:] )
subprocess.run( 'bld_fmu.py' + args, shell = True )
