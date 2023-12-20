#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-5 --dtInf=0.01 --out+S ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
