#!/usr/bin/env python
import subprocess, sys
args = ' ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w', newline = '\n' ) as log:
    subprocess.run( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
