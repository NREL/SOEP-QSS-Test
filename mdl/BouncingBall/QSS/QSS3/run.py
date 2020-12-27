#!/usr/bin/env python
import subprocess, sys
args = ' --zTol=1e-6 --dtInf=0.01 --dtOut=0.01 --out=ROZDSX ' + ' '.join( sys.argv[1:] ) # Good plots and fast
#args = ' --zTol=1e-6 --dtMax=0.01 ' + ' '.join( sys.argv[1:] ) # Good plots
#args = ' --zTol=1e-6 --dtInf=0.01 ' + ' '.join( sys.argv[1:] ) # Bad plots but fastest
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
