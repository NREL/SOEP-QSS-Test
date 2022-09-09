#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-4 --dtInf=0.001 --out=sROZDXL ' + ' '.join( sys.argv[1:] )
#args = ' --rTol=1e-6 --dtND=1e-4 --dtInf=0.001 --dtMax=0.01 ' + ' '.join( sys.argv[1:] ) # Using a tighter tolerance and dtMax gets closer to the correct/CVode simulation
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
