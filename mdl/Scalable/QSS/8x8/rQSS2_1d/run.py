#!/usr/bin/env python
import subprocess, sys
args = ' --relax --rTol=2.5e-6 --bin=U:0.2 --zFac=1000 --dtND=1e-4 --dtInf=0.2 --dtOut=1 --tEnd=86400 --out=sSROZDXQ ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )