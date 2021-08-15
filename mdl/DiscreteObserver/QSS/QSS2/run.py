#!/usr/bin/env python
import subprocess, sys
args = ' --dtMax=0.5 --dtND=1e-4 ' + ' '.join( sys.argv[1:] ) # Use dtMax to force some x requantizations to verify that y does observer updates
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
