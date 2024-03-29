#!/usr/bin/env python
import subprocess, sys
args = ' --zMul=50 --dtInf=0.01 --dtND=1e-4 ' + ' '.join( sys.argv[1:] ) # Need dtInf due to deactivation of u=sin(t) at t=0
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
