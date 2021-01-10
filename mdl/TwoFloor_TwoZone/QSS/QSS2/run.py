#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-2 --out=sROZDXL ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
