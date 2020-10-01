#!/usr/bin/env python
import subprocess, sys
args = ' --fxn=u:step[1,1,1] ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
