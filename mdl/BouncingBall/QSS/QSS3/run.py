#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-5 --zTol=1e-6 --dtInf=0.1 --dtMax=0.1 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
