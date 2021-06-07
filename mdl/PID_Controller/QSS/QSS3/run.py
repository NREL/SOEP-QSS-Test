#!/usr/bin/env python
import subprocess, sys
args = ' --zMul=20 --dtND=7e-3 ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
