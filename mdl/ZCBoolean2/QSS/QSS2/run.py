#!/usr/bin/env python
import subprocess, sys
args = ' --zFac=0.5 --dtMax=0.01 --dtND=1e-4 --out=sROZDXL ' + ' '.join( sys.argv[1:] ) # Need dtMax due to deactivation of u=sin(t) at t=0 # zFac<1 helps with ZC accuracy loss due to ND
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
