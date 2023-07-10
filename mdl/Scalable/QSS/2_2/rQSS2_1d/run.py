#!/usr/bin/env python
import subprocess, sys
args = ' --relax --rTol=5e-6 --bin=33:0.2:Y --zFac=1000 --dtND=1e-4 --dtInf=0.1 --dtOut=1 --tEnd=86400 --out=sSROZDXQ ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
