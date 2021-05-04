#!/usr/bin/env python
import subprocess, sys
args = ' --dtOut=100 --out=sSXL ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
