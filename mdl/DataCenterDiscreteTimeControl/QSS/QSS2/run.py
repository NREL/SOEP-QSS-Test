#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-4 --zMul=100 --dtOut=60 --out=sSXL ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
