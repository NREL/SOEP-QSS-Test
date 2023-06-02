#!/usr/bin/env python
import subprocess, sys
args = ' --bin=U:0.25:Y --dtND=1e-3 --dtInf=1 --dtOut=120 --out=sSROZDX ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
