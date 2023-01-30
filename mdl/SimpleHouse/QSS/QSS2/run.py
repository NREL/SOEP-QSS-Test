#!/usr/bin/env python
import subprocess, sys
args = ' --rTol=1e-6 --bin --dtND=5e-4 --out=sSROZDX --dtOut=3600 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
