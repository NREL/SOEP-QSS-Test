#!/usr/bin/env python
# FMU Build Script Wrapper
import subprocess, sys
args = ' ' + ' '.join( sys.argv[1:] )
subprocess.run( 'bld_fmu.py' + args, shell = True )
