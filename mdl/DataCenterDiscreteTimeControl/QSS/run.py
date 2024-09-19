#!/usr/bin/env python
import subprocess, sys
args = ' --bin=U:0.2 --dtND=1e-4 --zFac=100 --dtOut=100 --out=sSROZDXQ ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
