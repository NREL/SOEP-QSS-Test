#!/usr/bin/env python
# FMU Run Script Wrapper
import subprocess, sys
args = ' ' + ' '.join( sys.argv[1:] )
subprocess.run( 'run_fmu.py' + args, shell = True )
