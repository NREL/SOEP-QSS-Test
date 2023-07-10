#!/usr/bin/env python
import subprocess, sys
args = ' --rTol=1e-8 --maxh=0 --dtOut=1 --tEnd=86400 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
