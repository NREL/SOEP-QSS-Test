#!/usr/bin/env python
import subprocess, sys
args = '  ../../../Achilles1/OCT/Achilles1.fmu ../../../Achilles2/OCT/Achilles2.fmu --con=Achilles2.x1:Achilles1.x1 --con=Achilles1.x2:Achilles2.x2 --dtInf=0.001 --perfect --rTol=1e-8 --aTol=1e-10 --out=ROZDXK ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
