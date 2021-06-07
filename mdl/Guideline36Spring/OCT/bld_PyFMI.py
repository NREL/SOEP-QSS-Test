#!/usr/bin/env python
import subprocess, sys
args = ' --no-qss ' + ' '.join( sys.argv[1:] )
subprocess.run( 'bld_fmu.py' + args, shell = True )
