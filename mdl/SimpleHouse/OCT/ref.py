#!/usr/bin/env python
import subprocess, sys
args = ' --rTol=1e-8 --dtOut=60 ' + ' '.join( sys.argv[1:] )
with open( 'ref.log', 'w' ) as log:
    subprocess.run( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
