#!/usr/bin/env python
import subprocess, sys
args = ' --bin=5:0.25 --dtND=1e-4 --dtOut=100 --out=sSXL ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
