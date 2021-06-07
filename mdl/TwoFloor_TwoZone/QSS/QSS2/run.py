#!/usr/bin/env python
import subprocess, sys
args = ' --zrFac=100 --dtND=1e-4 --dtInf=0.001 --dtMax=0.01 --dtOut=100 --out=sROZDXQ ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
