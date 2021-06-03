#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=5e-2 --dtOut=100 --out=sROZDXQL ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
