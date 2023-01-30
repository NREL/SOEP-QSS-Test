#!/usr/bin/env python
import subprocess, sys
args = ' --bin --dtND=1e-4 --dtOut=100 --out=sSROZDX ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
