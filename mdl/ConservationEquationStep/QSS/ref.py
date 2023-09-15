#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-4 --dtOut=1 --out=dsSROZDXQ --rTol=1e-8 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
