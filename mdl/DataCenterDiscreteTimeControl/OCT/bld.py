#!/usr/bin/env python
import subprocess, sys
args = ' --no-dd ' + ' '.join( sys.argv[1:] )
subprocess.run( 'bld_fmu.py' + args, shell = True )
