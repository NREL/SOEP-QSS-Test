#!/usr/bin/env python
import subprocess, sys
args = ' --ncp=0 --tEnd=86400 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
