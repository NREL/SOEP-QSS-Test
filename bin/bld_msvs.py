#!/usr/bin/env python
# Default FMU Build Script Wrapper
import subprocess, sys
args = ' --msvs ' + ' '.join( sys.argv[1:] )
subprocess.run( 'bld_fmu.py' + args, shell = True )
