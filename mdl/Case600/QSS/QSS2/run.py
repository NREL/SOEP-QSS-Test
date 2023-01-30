#!/usr/bin/env python
import subprocess, sys
args = ' --zFac=10 --bin=40:0.3:Y --dtND=1e-4 --dtInf=1 --dtOut=100 --out=sSX ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
