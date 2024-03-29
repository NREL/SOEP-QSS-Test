#!/usr/bin/env python
import subprocess, sys
args = ' --rTol=5e-6 --bin=U:0.2 --zFac=1000 --dtND=1e-4 --dtInf=0.1 --dtOut=1 --tStop=86400 --out=sSROZDXQ ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
