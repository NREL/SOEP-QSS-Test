#!/usr/bin/env python
import subprocess, sys
args = ' --bin=50:0.4:Y --dtND=1e-4 --dtInf=1 --dtOut=100 --out=sSROZDX ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
