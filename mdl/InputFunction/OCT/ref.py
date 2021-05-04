#!/usr/bin/env python
import subprocess, sys
args = ' --inp=step --rTol=1e-8 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
