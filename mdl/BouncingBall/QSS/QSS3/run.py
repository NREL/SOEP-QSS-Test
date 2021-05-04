#!/usr/bin/env python
import subprocess, sys
args = ' --dtND=1e-4 --dtOut=0.001 --out=sROZDSX ' + ' '.join( sys.argv[1:] ) # Sampled output needed to see trajectories due to large steps
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
