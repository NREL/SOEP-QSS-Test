#!/usr/bin/env python
import subprocess, sys
args = ' --zFac=10 --dtND=1e-4 --dtInf=25 --dtOut=100 --out=sSXL ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
