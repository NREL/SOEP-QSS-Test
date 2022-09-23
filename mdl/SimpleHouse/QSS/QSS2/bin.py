#!/usr/bin/env python
import subprocess, sys
args = ' --bin=10:0.3 --dtND=5e-4 --out=sSX --dtOut=3600 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
