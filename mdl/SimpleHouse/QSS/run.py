#!/usr/bin/env python
import subprocess, sys
args = ' --rTol=5e-6 --zMul=1e6 --zrFac=1000 --bin=10:0.3 --dtND=2e-4 --dtOut=3600 --out=sSX ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w', newline = '\n' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
