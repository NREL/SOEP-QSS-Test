#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-4 --out=ds ' + ' '.join( sys.argv[1:] ) # This stops at 1.99s ZC
#args = ' --dtND=1e-4 --out=dsROZDX ' + ' '.join( sys.argv[1:] ) # This stalls at 1.99s ZC
#args = ' --dtND=1e-4 --dtMax=0.001 --out=dsROZDX ' + ' '.join( sys.argv[1:] ) # This finishes
#args = ' --dtND=1e-4 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
