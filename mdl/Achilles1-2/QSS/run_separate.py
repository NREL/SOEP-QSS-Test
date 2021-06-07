#!/usr/bin/env python
import subprocess, sys
args = '  ../../../Achilles1/OCT/Achilles1.fmu ../../../Achilles2/OCT/Achilles2.fmu --dtInf=0.001 --out=ROZDXK ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
