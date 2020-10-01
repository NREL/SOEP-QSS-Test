#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=2e-1 --dtOut=100 --out=Fsx ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
