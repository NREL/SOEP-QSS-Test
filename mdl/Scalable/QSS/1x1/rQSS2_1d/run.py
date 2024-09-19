#!/usr/bin/env python
import subprocess, sys
args = ' --rTol=5e-6 --bin=33:0.2 --zFac=1000 --dtND=1e-4 --tStop=86400 --out=sROZDXQ ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
